import numpy as np
import random
import configparser

from .visualize import save_img, group_images
from .common import readImg
from .pre_processing import my_PreProc

                                                                                         
                           
def load_file_path_txt(file_path):
    img_list = []
    gt_list = []
    fov_list = []
    with open(file_path, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline().strip()               
            if not lines:
                break
            img,gt,fov = lines.split(' ')
            img_list.append(img)
            gt_list.append(gt)
            fov_list.append(fov)
    return img_list,gt_list,fov_list

                                                                                                  
def load_data(data_path_list_file):
    print('\033[0;33mload data from {} \033[0m'.format(data_path_list_file))
    img_list, gt_list, fov_list = load_file_path_txt(data_path_list_file)
    imgs = None
    groundTruth = None
    FOVs = None
    for i in range(len(img_list)):
        img = np.asarray(readImg(img_list[i]))
        gt = np.asarray(readImg(gt_list[i]))
        if len(gt.shape)==3:
            gt = gt[:,:,0]
        fov = np.asarray(readImg(fov_list[i]))
        if len(fov.shape)==3:
            fov = fov[:,:,0]

        imgs = np.expand_dims(img,0) if imgs is None else np.concatenate((imgs,np.expand_dims(img,0)))
        groundTruth = np.expand_dims(gt,0) if groundTruth is None else np.concatenate((groundTruth,np.expand_dims(gt,0)))
        FOVs = np.expand_dims(fov,0) if FOVs is None else np.concatenate((FOVs,np.expand_dims(fov,0)))
    
    assert(np.min(FOVs)==0 and np.max(FOVs)==255)
    assert((np.min(groundTruth)==0 and (np.max(groundTruth)==255 or np.max(groundTruth)==1)))                                
    if np.max(groundTruth)==1:
        print("\033[0;31m Single channel binary image is multiplied by 255 \033[0m")
        groundTruth = groundTruth * 255

                                               
    imgs = np.transpose(imgs,(0,3,1,2))
    groundTruth = np.expand_dims(groundTruth,1)
    FOVs = np.expand_dims(FOVs,1)
    print('ori data shape < ori_imgs:{} GTs:{} FOVs:{}'.format(imgs.shape,groundTruth.shape,FOVs.shape))
    print("imgs pixel range %s-%s: " %(str(np.min(imgs)),str(np.max(imgs))))
    print("GTs pixel range %s-%s: " %(str(np.min(groundTruth)),str(np.max(groundTruth))))
    print("FOVs pixel range %s-%s: " %(str(np.min(FOVs)),str(np.max(FOVs))))
    print("==================data have loaded======================")
    return imgs, groundTruth, FOVs

                                                                                            
                                                                     
def get_data_train(data_path_list,patch_height,patch_width,N_patches,inside_FOV):
    train_imgs_original, train_masks, train_FOVs = load_data(data_path_list)
                                                                                                                     

    train_imgs = my_PreProc(train_imgs_original)
    train_masks = train_masks/255.
    train_FOVs = train_FOVs//255
    
                          
                                               
                                              
                                            

                      
    data_dim_check(train_imgs,train_masks)  
    assert(np.min(train_masks)==0 and np.max(train_masks)==1)
    assert(np.min(train_FOVs)==0 and np.max(train_FOVs)==1)
                               
    print("\nTrain images shape: {}, vaule range ({} - {}):"\
        .format(train_imgs.shape, str(np.min(train_imgs)), str(np.max(train_imgs))))

                                              
    patches_imgs_train, patches_masks_train = extract_random(train_imgs,train_masks,train_FOVs,patch_height,patch_width,N_patches,inside_FOV)
    data_dim_check(patches_imgs_train, patches_masks_train)

    print("train patches shape: {}, value range ({} - {})"\
        .format(patches_imgs_train.shape, str(np.min(patches_imgs_train)), str(np.max(patches_imgs_train))))

    return patches_imgs_train, patches_masks_train

                                                 
def extract_random(full_imgs,full_masks,full_FOVs, patch_h,patch_w, N_patches, inside='not'):
    patch_per_img = int(N_patches/full_imgs.shape[0])
    if (N_patches%full_imgs.shape[0] != 0):
        print("\033[0;31mRecommended N_patches be set as a multiple of train img numbers\033[0m")
        N_patches = patch_per_img * full_imgs.shape[0]
    print("patches per image: " +str(patch_per_img), "  Total number of patches:", N_patches)
    patches = np.empty((N_patches,full_imgs.shape[1],patch_h,patch_w))
    patches_masks = np.empty((N_patches,full_masks.shape[1],patch_h,patch_w), dtype=np.uint8)
    img_h = full_imgs.shape[2]                      
    img_w = full_imgs.shape[3]                    

    iter_tot = 0                                                     
    for i in range(full_imgs.shape[0]):                           
        k=0
        while k <patch_per_img:
            x_center = random.randint(0+int(patch_w/2),img_w-int(patch_w/2))
            y_center = random.randint(0+int(patch_h/2),img_h-int(patch_h/2))
                                                            
            if inside=='center' or inside == 'all':
                if not is_patch_inside_FOV(x_center,y_center,full_FOVs[i,0],patch_h,patch_w,mode=inside):
                    continue
            patch = full_imgs[i,:,y_center-int(patch_h/2):y_center+int(patch_h/2),x_center-int(patch_w/2):x_center+int(patch_w/2)]
            patch_mask = full_masks[i,:,y_center-int(patch_h/2):y_center+int(patch_h/2),x_center-int(patch_w/2):x_center+int(patch_w/2)]
            patches[iter_tot]=patch
            patches_masks[iter_tot]=patch_mask
            iter_tot +=1         
            k+=1               
    return patches, patches_masks

def is_patch_inside_FOV(x,y,fov_img,patch_h,patch_w,mode='center'):
    if mode == 'center':
        return fov_img[y,x]
    elif mode == 'all':
        fov_patch = fov_img[y-int(patch_h/2):y+int(patch_h/2),x-int(patch_w/2):x+int(patch_w/2)]
        return fov_patch.all()
    else:
        raise ValueError("\033[0;31mmode is incurrent!\033[0m")

                        
def data_dim_check(imgs,masks):
    assert(len(imgs.shape)==len(masks.shape))
    assert(imgs.shape[0]==masks.shape[0])
    assert(imgs.shape[2]==masks.shape[2])
    assert(imgs.shape[3]==masks.shape[3])
    assert(masks.shape[1]==1)
    assert(imgs.shape[1]==1 or imgs.shape[1]==3)

                                                                                       
                                                                     
                                               
def get_data_test_overlap(test_data_path_list, patch_height, patch_width, stride_height, stride_width):
    test_imgs_original, test_masks, test_FOVs= load_data(test_data_path_list)

    test_imgs = my_PreProc(test_imgs_original)
    test_masks = test_masks/255.
    test_FOVs = test_FOVs//255
                                                                                          
    test_imgs = paint_border_overlap(test_imgs, patch_height, patch_width, stride_height, stride_width)

                               
    assert(np.max(test_masks)==1  and np.min(test_masks)==0)
    print("\nTest images shape: {}, vaule range ({} - {}):"\
        .format(test_imgs.shape, str(np.min(test_imgs)), str(np.max(test_imgs))))

                                                      
    patches_imgs_test = extract_ordered_overlap(test_imgs,patch_height,patch_width,stride_height,stride_width)
    print("test patches shape: {}, value range ({} - {})"\
        .format(patches_imgs_test.shape, str(np.min(patches_imgs_test)), str(np.max(patches_imgs_test))))

    return patches_imgs_test, test_imgs_original, test_masks, test_FOVs, test_imgs.shape[2], test_imgs.shape[3]

                                                                                       
def paint_border_overlap(full_imgs, patch_h, patch_w, stride_h, stride_w):
    assert (len(full_imgs.shape)==4)            
    assert (full_imgs.shape[1]==1 or full_imgs.shape[1]==3)                               
    img_h = full_imgs.shape[2]                      
    img_w = full_imgs.shape[3]                    
    leftover_h = (img_h-patch_h)%stride_h                        
    leftover_w = (img_w-patch_w)%stride_w                        
    if (leftover_h != 0):                            
        print("\nthe side H is not compatible with the selected stride of " +str(stride_h))
                                                                                                 
        print("(img_h - patch_h) MOD stride_h: " +str(leftover_h))
        print("So the H dim will be padded with additional " +str(stride_h - leftover_h) + " pixels")
        tmp_full_imgs = np.zeros((full_imgs.shape[0],full_imgs.shape[1],img_h+(stride_h-leftover_h),img_w))
        tmp_full_imgs[0:full_imgs.shape[0],0:full_imgs.shape[1],0:img_h,0:img_w] = full_imgs
        full_imgs = tmp_full_imgs
    if (leftover_w != 0):                             
        print("the side W is not compatible with the selected stride of " +str(stride_w))
                                                                                                 
        print("(img_w - patch_w) MOD stride_w: " +str(leftover_w))
        print("So the W dim will be padded with additional " +str(stride_w - leftover_w) + " pixels")
        tmp_full_imgs = np.zeros((full_imgs.shape[0],full_imgs.shape[1],full_imgs.shape[2],img_w+(stride_w - leftover_w)))
        tmp_full_imgs[0:full_imgs.shape[0],0:full_imgs.shape[1],0:full_imgs.shape[2],0:img_w] = full_imgs
        full_imgs = tmp_full_imgs
    print("new padded images shape: " +str(full_imgs.shape))
    return full_imgs

                                                 
def extract_ordered_overlap(full_imgs, patch_h, patch_w,stride_h,stride_w):
    assert (len(full_imgs.shape)==4)            
    assert (full_imgs.shape[1]==1 or full_imgs.shape[1]==3)                              
    img_h = full_imgs.shape[2]                           
    img_w = full_imgs.shape[3]                         
    assert ((img_h-patch_h)%stride_h==0 and (img_w-patch_w)%stride_w==0)
    N_patches_img = ((img_h-patch_h)//stride_h+1)*((img_w-patch_w)//stride_w+1)                                   
    N_patches_tot = N_patches_img*full_imgs.shape[0]
    print("Number of patches on h : " +str(((img_h-patch_h)//stride_h+1)))
    print("Number of patches on w : " +str(((img_w-patch_w)//stride_w+1)))
    print("number of patches per image: " +str(N_patches_img) +", totally for testset: " +str(N_patches_tot))
    patches = np.empty((N_patches_tot,full_imgs.shape[1],patch_h,patch_w))
    iter_tot = 0                                                     
    for i in range(full_imgs.shape[0]):                            
        for h in range((img_h-patch_h)//stride_h+1):
            for w in range((img_w-patch_w)//stride_w+1):
                patch = full_imgs[i,:,h*stride_h:(h*stride_h)+patch_h,w*stride_w:(w*stride_w)+patch_w]
                patches[iter_tot]=patch
                iter_tot +=1         
    assert (iter_tot==N_patches_tot)
    return patches                                                  

                                                   
def recompone_overlap(preds, img_h, img_w, stride_h, stride_w):
    assert (len(preds.shape)==4)            
    assert (preds.shape[1]==1 or preds.shape[1]==3)                              
    patch_h = preds.shape[2]
    patch_w = preds.shape[3]
    N_patches_h = (img_h-patch_h)//stride_h+1
    N_patches_w = (img_w-patch_w)//stride_w+1
    N_patches_img = N_patches_h * N_patches_w
                                               
                                               
                                                   
    assert (preds.shape[0]%N_patches_img==0)
    N_full_imgs = preds.shape[0]//N_patches_img
    print("There are " +str(N_full_imgs) +" images in Testset")
    full_prob = np.zeros((N_full_imgs,preds.shape[1],img_h,img_w))
    full_sum = np.zeros((N_full_imgs,preds.shape[1],img_h,img_w))

    k = 0                               
    for i in range(N_full_imgs):
        for h in range((img_h-patch_h)//stride_h+1):
            for w in range((img_w-patch_w)//stride_w+1):
                full_prob[i,:,h*stride_h:(h*stride_h)+patch_h,w*stride_w:(w*stride_w)+patch_w]+=preds[k]                              
                full_sum[i,:,h*stride_h:(h*stride_h)+patch_h,w*stride_w:(w*stride_w)+patch_w]+=1                                        
                k+=1
    assert(k==preds.shape[0])
    assert(np.min(full_sum)>=1.0) 
    final_avg = full_prob/full_sum                   
                            
    assert(np.max(final_avg)<=1.0)                               
    assert(np.min(final_avg)>=0.0)                               
    return final_avg

                                                                                 
def pred_only_in_FOV(data_imgs,data_masks,FOVs):
    assert (len(data_imgs.shape)==4 and len(data_masks.shape)==4)            
    height = data_imgs.shape[2]
    width = data_imgs.shape[3]
    new_pred_imgs = []
    new_pred_masks = []
    for i in range(data_imgs.shape[0]):                                
        for x in range(width):
            for y in range(height):
                if pixel_inside_FOV(i,x,y,FOVs):
                    new_pred_imgs.append(data_imgs[i,:,y,x])
                    new_pred_masks.append(data_masks[i,:,y,x])
    new_pred_imgs = np.asarray(new_pred_imgs)
    new_pred_masks = np.asarray(new_pred_masks)
    return new_pred_imgs, new_pred_masks

                                                              
def kill_border(data, FOVs):
    assert (len(data.shape)==4)            
    assert (data.shape[1]==1 or data.shape[1]==3)                              
    height = data.shape[2]
    width = data.shape[3]
    for i in range(data.shape[0]):                            
        for x in range(width):
            for y in range(height):
                if not pixel_inside_FOV(i,x,y,FOVs):
                    data[i,:,y,x]=0.0

                                            
def pixel_inside_FOV(i, x, y, FOVs):
    assert (len(FOVs.shape)==4)            
    assert (FOVs.shape[1]==1)
    if (x >= FOVs.shape[3] or y >= FOVs.shape[2]):                                 
        return False
    return FOVs[i,0,y,x]>0                 


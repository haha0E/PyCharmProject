class boy:
    name = ''


s = 'this ' 'is ' 'string'
if __name__ == '__main__':
    '''mmpose 测试'''
    from mmpose.apis import (init_pose_model, inference_bottom_up_pose_model, vis_pose_result,webcam)

    config_file = 'associative_embedding_hrnet_w32_coco_512x512.py'
    checkpoint_file = 'hrnet_w32_coco_512x512-bcb8c247_20200816.pth'
    pose_model = init_pose_model(config_file, checkpoint_file, device='cuda:0')  # or device='cpu'

    image_name = "E:\picture\本机照片\WIN_20230404_16_43_36_Pro.jpg"
    # 接受图片
    image = image_name
    newimg ="E:\download\WIN_20230404_16_43_36_Pro.png"
    # 使用mmpose中的自底向上模型生成人体关键节点
    pose_results, _ = inference_bottom_up_pose_model(pose_model, image_name)
    # 把关键点绘制到帧上显示出来
    vis_pose_result(pose_model, image, pose_results, out_file='vis_persons.jpg')
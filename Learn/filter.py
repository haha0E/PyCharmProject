import math

from fastdtw import fastdtw
from mmpose.apis import (init_pose_model)


def cal_distance(point_a, point_b):
    a_x, b_x = point_a[0], point_b[0]
    a_y, b_y = point_a[1], point_b[1]
    distance = math.sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)
    return distance


def cal_angle(point_a, point_b, point_c):
    a_x, b_x, c_x = point_a[0], point_b[0], point_c[0]
    a_y, b_y, c_y = point_a[1], point_b[1], point_c[1]
    x1, y1 = (a_x - b_x), (a_y - b_y)
    x2, y2 = (c_x - b_x), (c_y - b_y)
    cos_b = (x1 * x2 + y1 * y2) / (math.sqrt(x1 ** 2 + y1 ** 2) * math.sqrt(x2 ** 2 + y2 ** 2))
    return cos_b


def get_points_and_cal(pose_result):
    eigenvalue = [];
    keypoints = pose_result[0][0]['keypoints']
    left_shoulder = keypoints[5];
    right_shoulder = keypoints[6]
    left_elbow = keypoints[7];
    right_elbow = keypoints[8]
    left_hand = keypoints[9];
    right_hand = keypoints[10]
    left_hip = keypoints[11];
    right_hip = keypoints[12]
    left_knee = keypoints[13];
    right_knee = keypoints[14]
    left_ankle = keypoints[15];
    right_ankle = keypoints[16]
    lhand_lshoulder = cal_distance(left_hand, left_shoulder)
    rhand_rshoulder = cal_distance(right_hand, right_shoulder)
    lelbow_lshoulder = cal_distance(left_elbow, left_shoulder)
    relbow_rshoulder = cal_distance(right_elbow, right_shoulder)
    lknee_lhip = cal_distance(left_knee, left_hip)
    rknee_rhip = cal_distance(right_knee, right_hip)
    lankle_lhip = cal_distance(left_ankle, left_hip)
    rankle_rhip = cal_distance(right_ankle, right_hip)
    distances = [lhand_lshoulder, rhand_rshoulder, lelbow_lshoulder, relbow_rshoulder, lknee_lhip, rknee_rhip,
                 lankle_lhip, rankle_rhip]
    larm_body = cal_angle(left_hand, left_shoulder, left_hip)
    rarm_rbody = cal_angle(right_hand, right_shoulder, right_hip)
    lhand_larm = cal_angle(left_shoulder, left_elbow, left_hand)
    rhand_rarm = cal_angle(right_shoulder, right_elbow, right_hand)
    lleg = cal_angle(left_hip, left_knee, left_ankle)
    rleg = cal_angle(right_hip, right_knee, right_ankle)
    lleg_body = cal_angle(left_knee, left_hip, left_shoulder)
    rleg_body = cal_angle(right_knee, right_hip, right_shoulder)
    angles = [larm_body, rarm_rbody, lhand_larm, rhand_rarm, lleg, rleg, lleg_body, rleg_body]
    eigenvalue.append(angles)
    eigenvalue.append(distances)
    return eigenvalue


config_file = 'associative_embedding_hrnet_w32_coco_512x512.py'
checkpoint_file = 'hrnet_w32_coco_512x512-bcb8c247_20200816.pth'
pose_model = init_pose_model(config_file, checkpoint_file, device='cuda:0')  # or device='cpu'

video_1 = 'videos/WIN_20230404_22_58_43_Pro.mp4'
video_2 = 'videos/WIN_20230404_22_59_11_Pro.mp4'


def match_cal(path, seq1, seq2, weight):
    # 对两个集合进行L2范数归一化
    l1 = 0;
    l2 = 0;
    for a in seq1:
        l1 += a;
    for b in seq2:
        l2 += b;
    l1 = math.sqrt(l1)
    l2 = math.sqrt(l2)
    for i in range(0, len(seq1)):
        seq1[i] /= l1
    for i in range(0, len(seq2)):
        seq2[i] /= l2
    # 求权重之和用于加权平均
    sum = 0
    for i in weight:
        sum += i
    ans = 0;
    for i, j in path:
        similar = 0
        for a, b, c in seq1[i], seq2[j], weight:
            similar += (a - b) ** 2 * weight[i]
        similar /= sum
        similar = math.sqrt(similar)
        ans += similar
    ans /= len(path)
    return ans


def get_weight(move):
    return 0


def get_firstframe(move):
    return 0


def get_eigenvalue(move):
    return 0


seq = []
begin = False
mistake = ''
count = 0



def real_time_match_cal(frame, move):  # frame是视频流的最新一帧，move是动作id
    firstframe = get_firstframe(move)  # 数据库中找到该动作的第一帧
    weight = get_weight(move)
    # 进行新一次的错误警示
    global begin, seq, mistake, count
    seq = []
    mistake = []
    avg = 0
    count = 0
    sw = sum(weight)
    # 判断与第一帧相似度
    for i, j, w in firstframe, frame, weight:
        avg += firstframe / frame * w
    avg /= sw
    if avg >= 0.75:  # 周期是否开始
        seq.append(frame)
        begin = not begin
        count += 1
    if begin:
        seq.append()
    elif count == 2:
        standard = get_eigenvalue(move)  # 获取标准数据的特征值序列
        distance, path = fastdtw(standard, seq)
        x = match_cal(path, standard, seq, weight)
    if x < 0.6:
        mistake = '出现错误，请注意体态'


if __name__ == '__main__':
    print('hello')

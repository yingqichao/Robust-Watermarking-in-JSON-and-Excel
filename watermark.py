import json
import random
import math
import struct



if __name__ == "__main__":
    # JSON = {"logData":{"eventInfo":{"securemode":1,"eventType":306,           "detectStart"        : 1554083172.2377,  "subtype": 3   , "reqid":"275765ca16d63d39d5","ipcType":2,"taskid":"1711","home":"0","type":3,"createtime":"1554083135","alarmtype":6,"sn":"360T0528748","detectEnd":1554083187.654,"detectSpent":15.416320085526},"imageInfo":{"duration":35000,"snapshot":"2cd251950b69d6bfda28b69a1cb17ca44367ec5d-3-2-3-768-688.jpg","createtime":1554083172,"videokey":"97b4656a876fca3072848c2300e15601076bf4f7-2-10-3.mp4","videosize":3498972},"options":{"bindInfo":{"status":"0","acl_info":"{\"acl1\":\"1\",\"acl2\":\"1\",\"acl3\":\"1\",\"acl4\":\"0\",\"acl5\":\"1\"}","extend":None,"deleted":"0","qid":"978315492","bind_qid":"978315492","ts":"352471000","id":"935937862","play_num":"4","play_key":"691c9e76ed9b9ba6f5c864bd6bf7591f","create_time":"2019-02-05 15:41:11","role":"0","sn":"360T0528748","operator":"","is_public":"0","play_time":"2019-03-01 22:53:07","share_num":"0","modify_time":"2019-03-05 16:38:09"},"detectFace":{"msg":"ok","data":{"find_body":True,"find_face":False,"video_url":"http:\/\/q3.jia.360.cn:8360\/image\/viewVideo?videoKey=97b4656a876fca3072848c2300e15601076bf4f7-2-10-3.mp4&sn=360T0528748&sign=c8610cc0a6c2de7dba840915719afff5&signTS=1554083172","face_frame_index":-1,"qid":"978315492","body_frame_index":0,"body_rect":[341,289,80,236],"image_id":"http:\/\/q3.jia.360.cn:8360\/image\/viewVideo?videoKey=97b4656a876fca3072848c2300e15601076bf4f7-2-10-3.mp4&sn=360T0528748&sign=c8610cc0a6c2de7dba840915719afff5&signTS=1554083172","FPS":20.008238,"type":"video","group_id":-1,"user_name":"","face_image_len":53696},"func":"get_face_info","rc":0}}},"result":True,"timeoutRet":1}
    # print(
    #     json.dumps(
    #     JSON, sort_keys=True, indent=4, separators=(',', ': ')
    #     )
    # )

    with open('original.txt', 'r') as f:
        JSON = json.load(f)
        # print(JSON)

    #打印JSON
    map = json.dumps(
        JSON, sort_keys=True, indent=4, separators=(',', ': ')
    )
    print(map)

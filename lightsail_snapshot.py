import boto3
import datetime

### variable
INSTANCE_NAME = 'WordPress-512MB-Tokyo-1'
GENERATIONS = 4

### 
old_Snapshot_number = 0
create_date = []

#def support_datetime_default(o):
#    if isinstance(o, datetime):
#        return o.isoformat()
#    raise TypeError(repr(o) + "aaaaa")

def GetSnapshotName():
    d_now = datetime.datetime.now()
    filename = INSTANCE_NAME+"_snapshot_"+d_now.strftime('%Y%m%d%H%M%S')
    return filename

def DecideDeleteSnapshot(dict,number):
    global old_Snapshot_number

    for i in range(0,number):
        create_date.append(dict['instanceSnapshots'][i]['createdAt'])

    for j in range(0,number):
        if j == 0:
            old_create_date = create_date[j]
        else:
            if old_create_date >= create_date[j]:
                old_create_date = create_date[j]
                old_Snapshot_number = j

    return old_Snapshot_number

def CreateSnapshot(client,snapshot_filename):
    client.create_instance_snapshot(
            instanceSnapshotName=snapshot_filename,
            instanceName=INSTANCE_NAME,
    )

def DeleteSnapshot(client,responce,DeleteNumber):
    client.delete_instance_snapshot(
            instanceSnapshotName=responce['instanceSnapshots'][DeleteNumber]['name']
    )

def lambda_handler(event, context):
    filename = GetSnapshotName()
    client = boto3.client('lightsail')
    #instance_json = json.dumps(instance_dict, default=support_datetime_default)
    responce = client.get_instance_snapshots()
    instances_number = len(responce['instanceSnapshots'])
    if instances_number < GENERATIONS:
        CreateSnapshot(client,filename)
    else:
        d = DecideDeleteSnapshot(responce,instances_number)
        DeleteSnapshot(client,responce,d)
        CreateSnapshot(client,filename)

#if __name__ == "__main__":
#    main()
# __name__は特殊な変数。モジュールインポート時の__name__はXXX.pyのXXXとなる。
# python XXX.pyとで実行した場合は、"__main__"となるとのこと。
# ちゃんとpython XXX.py と実行した場合に動作させるよっておまじない。

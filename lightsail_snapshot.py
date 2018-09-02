import boto3
import datetime

### variable
INSTANCE_NAME = 'XXX'
GENERATIONS = 4

def GetSnapshotName():
    d_now = datetime.datetime.now()
    filename = INSTANCE_NAME+"_snapshot_"+d_now.strftime('%Y%m%d%H%M%S')
    return filename

def CreateSnapshot(client,INSTANCE_NAME):
    new_snapshot_name = GetSnapshotName()

    client.create_instance_snapshot(
            instanceSnapshotName=new_snapshot_name,
            instanceName=INSTANCE_NAME,
    )
    print(f"{snapshot_filename} is created.")

def DeleteSnapshot(client,INSTANCE_NAME):
    all_snapshots_list_responce = client.get_instance_snapshots()
    filterd_snapshots_list = filter(lambda x: x['fromInstanceName'] == INSTANCE_NAME, all_snapshots_list_responce['instanceSnapshots'])
    sorted_list = sorted(filterd_snapshots_list, key=lambda x:x['createdAt'])

    if len(sorted_list) >= GENERATIONS:
        old_snapshot = sorted_list[0]
        old_snapshot_name = old_snapshot['name']
        client.delete_instance_snapshot(
            instanceSnapshotName=old_snapshot_name
        )
        print(f"{old_snapshot_name} is deleted.")
    else:
        print(f"snapshot is not deleted.")

def lambda_handler(event, context):
    client = boto3.client('lightsail')
    CreateSnapshot(client,INSTANCE_NAME)
    DeleteSnapshot(client,INSTANCE_NAME)

#if __name__ == "__main__":
#    main()

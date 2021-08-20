from services.firestore import FirestoreService

firestore = FirestoreService()

configs = firestore.get_configs()
print(configs[0])

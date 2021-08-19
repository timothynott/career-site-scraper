from services.firestore import Firestore

firestore = Firestore()

configs = firestore.get_configs()
print(configs[0])

from deepface import DeepFace

class FaceRecognition:
    def __init__(self):
        pass

    def check_match(self, img_path, db_path):
        dfs = DeepFace.find(img_path=img_path, db_path=db_path)
        match_found = any(len(df['distance']) > 0 for df in dfs)
        if match_found:
            filename = dfs[0].iloc[0]['identity']
            # Split after '\' and then extract substring before ".jpeg"
            filename_parts = filename.split('\\')
            filename_before_dot = filename_parts[-1].split(".jpeg")[0]
            return True, filename_before_dot
        else:
            return False, None

import json
import uuid
import language_loader

def get_uuid1():
        data = language_loader.data
        if len(data["uuid"].strip()) == 0:
            new_uuid = uuid.uuid1()
            data["uuid"] = str(new_uuid)
            with open("launch_options.json", "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            return new_uuid
        return data["uuid"].strip()

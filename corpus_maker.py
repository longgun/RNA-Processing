import yaml
from yaml.loader import FullLoader


class PreProcesser:
    def __init__(self, config_path="./config.yaml"):
        with open(config_path) as yml:
            self.config = yaml.load(yml, Loader=FullLoader)
        print(self.config)

    def main(self):
        pass


if __name__ == "__main__":
    OBJ = PreProcesser()
    OBJ.main()
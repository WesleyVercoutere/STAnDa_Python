import glob


class RecipeManager:

    def __init__(self, folder) -> None:
        self.folder = folder
        self.filenames = list()
        self.recipes = set()
        
    def run(self):
        self._getFiles()
        self._collectRecipe()
        self._output()
        
    def _getFiles(self):
        self.filenames = glob.glob(self.folder + "/*.csv") 

    def _collectRecipe(self):

        for name in self.filenames:
            recipe = ""

            filename = name.split("\\")[-1]
            filename = filename.split("_")

            recipe = filename[3]

            if recipe != "":
                self.recipes.add(recipe)

    def _output(self):
        [print(i) for i in self.recipes]


if __name__ == "__main__":

    folder = r"E:\Gilbos Machines\SmarTwist\Maintenance\20210824 Dixie\CTS data\W2021_32_33 na update"

    app = RecipeManager(folder)
    app.run()

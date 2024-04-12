from RLL_Snippet_Generator import WordSnippetLocation as WSL
import os
import RLL_Snippet_Generator.SnippetGenerator as SG

""" Takes paths to the snippets tsv directory, the image tar directory, and the image json tar directory
and generates the snippet images then saves them in directories within the parent baseDir directory.

:param snippetsTsvDir_path: path to the snippets tsv directory.
:param imagesTsv_path: path to the image tar directory.
:param jsonsTar_path: path to the image json tar directory.
:param outputDir_path: path for output directory.

"""


class ProcessWordSnippets:
    @staticmethod
    def process_word_snippets(snippetsTsvDir_path: str, imagesTar_path: str, jsonsTar_path: str,
                              outputDir_path: str) -> None:
        sg = SG.SnippetGenerator(imagesTar_path, jsonsTar_path)
        tsvSet = os.listdir(snippetsTsvDir_path)

        if not (os.path.exists(outputDir_path)):
            os.mkdir(outputDir_path)

        sg.extract_json(jsonsTar_path)  # added?

        for image, imgName in sg.image_from_tar_generator(imagesTar_path):
            rootName = imgName.split('.')[0]
            tsvName = rootName + ".tsv"
            imageDir = os.path.join(outputDir_path, rootName)
            os.mkdir(imageDir)
            if tsvName in tsvSet:
                tsvPath = os.path.join(snippetsTsvDir_path, tsvName)
                wordLocations = WSL.get_word_locations_from_tsv(tsvPath)
                for snippet, snpName in sg.image_snippet_generator(image, imgName, wordLocations, False):
                    rootName = snpName.split('.')[0]
                    snippetPath = os.path.join(imageDir, rootName + ".jpg")
                    snippet.save(snippetPath, 'JPEG')

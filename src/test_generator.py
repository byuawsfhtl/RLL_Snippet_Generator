from SnippetGenerator import SnippetGenerator as sg
import pandas as pd

df = pd.read_csv(r"C:\Users\Jackson Roubidoux\RLL\repos\RLL_Snippet_Generator\tests\resources\images.tsv", sep='\t')
tar_path = r"C:\Users\Jackson Roubidoux\RLL\repos\RLL_Snippet_Generator\tests\resources\images.tar"
outdir = r"C:\Users\Jackson Roubidoux\RLL\repos\RLL_Snippet_Generator\src"

snippet_generator = sg(df)

snippet_generator.save_snippets_as_tar(tar_path, outdir)
snippet_generator.save_snippets_to_directory(tar_path, outdir)
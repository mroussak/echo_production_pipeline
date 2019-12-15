import Components.DataParser.DataParserFunctions as funcs
import Tools.DatabaseTools as tools
import os


def main(file_paths):
    
    # unpack file paths:
    videos_table_file_path = file_paths['videos_table']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), **tools.kwargs)
    
    # Step 2, get root paths:
    root_paths = funcs.GetRootFolders()
    
    # Step 3, get list of folders:
    videos_table = funcs.GetFilePaths(root_paths)
    
    # Step 4, rename jpegs with leading zeros:
    funcs.RenameJpegs(videos_table)
    
    # Step 5, parse data:
    videos_table = funcs.ParseVideosTable(videos_table)
    
    # Step 6, export data:
    tools.ExportDataToFile(videos_table, videos_table_file_path)
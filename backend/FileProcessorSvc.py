from FileProcessor import FileProcessor


class FileProcessorSvc:
    @staticmethod
    def get_all_file_names():
        return FileProcessor().retrieve_file_names()

    @staticmethod
    def upload_file(file_name, file_path):
        return FileProcessor().upload_file(file_name, file_path)

    @staticmethod
    def delete_file(file_name):
        return FileProcessor().delete_file(file_name)

    @staticmethod
    def get_download_url(file_name):
        return FileProcessor().fetch_file_url(file_name)

from config import *
import multiprocessing
from utils import load_json
from raw_data import OpenSea_accs

#TODO
# Распараллелить парс на несколько процессов, тем самым увеличив скорость обработки
# Переделать под обьктную базу
# Логгирование

class ParseManger:
    def __init__(self, urls, workClass) -> None:
        self.urls = urls
        self.workClass = workClass

    def run_script(self,url_queue):
        while True:
            try:
                parser = self.workClass()
                url = url_queue.get(timeout=1)  # Получаем доступную ссылку из очереди
                parser.run(url)
                url_queue.task_done()
            except multiprocessing.Queue.Empty:
                break  # Если очередь пуста, завершаем работу процесса



    def start_processes(self, process_count=4):
        url_queue = multiprocessing.JoinableQueue()
        
        for url in self.urls:
            url_queue.put(url)

        processes = []
        for _ in range(process_count):
            p = multiprocessing.Process(target=self.run_script, args=(url_queue,))
            p.start()
            processes.append(p)

        url_queue.join()

        # Ожидаем завершения всех процессов
        for p in processes:
            p.join()








if __name__ == "__main__":    
    #processing_data_from_nft_json("Cool Cats NFT", 2000)
    #get_all_nfts_url()
    #print(len(set(load_json("Cool Cats NFT"))))
    #print(len(remove_proccesed_data("Cool Cats NFT")))

    #ParseManger(load_json("nfts_list")[7:],OpenSea_accs).start_processes()
    OpenSea_accs().run("https://opensea.io/collection/gemesis")
    # for url in load_json("nfts_list")[7:]:
    #     scrap_accUrl_from_nft_page(url)




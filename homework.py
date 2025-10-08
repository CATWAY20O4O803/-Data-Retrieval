import re
import sys
from typing import List, Tuple, Dict, Any


class InvertedIndex:

    def __init__(self):
        self.inverted_lists: Dict[str, List[int]] = {}  
        self.records: List[Tuple[str, str]] = []        

    def build_from_file(self, file_name: str):

        print(f"正在從檔案 '{file_name}' 讀取並建構索引...")
        
        with open(file_name, "rb") as file:
            record_id = 0
            for binary_line in file:
                try:
                    line = binary_line.decode("utf-8", errors='ignore')
                except Exception:
                    # 如果連嘗試解碼都失敗會跳過
                    continue

                try:
                    # 使用 split("\t", 2) 只分割前兩個 Tab，其餘視為第三部分
                    parts = line.strip().split("\t", 2)
                    if len(parts) < 2:
                         continue # 跳過不符合格式的行
                    title = parts[0]
                    description = parts[1]
                except Exception:
                    continue
                
                # 儲存記錄資料，索引位置即為記錄 ID (Record ID)
                self.records.append((title, description))

                # 2. Tokenize 並建構索引
                # 結合標題和描述進行索引
                text = title + " " + description
                # 簡單分詞：使用正則表達式找出所有單字，並轉為小寫
                words = [word.lower() for word in re.findall(r"\w+", text) if word]
                
                # 使用一個 set 來追蹤此記錄中已處理過的單字，以確保記錄 ID 只被新增一次
                unique_words_in_record = set() 
                
                for word in words:
                    if word not in unique_words_in_record:
                        
                        # 確保該單字的倒排列表已存在
                        if word not in self.inverted_lists:
                            self.inverted_lists[word] = []
                        
                        # 將記錄 ID 新增到倒排列表
                        self.inverted_lists[word].append(record_id)
                        
                        # 將單字標記為已處理
                        unique_words_in_record.add(word)
                
                record_id += 1
        print("索引建構完成。")

    @staticmethod
    def intersect(list1: List[int], list2: List[int]) -> List[int]:
        """
        計算兩個已排序的倒排列表（記錄 ID 列表）的交集。
        
        執行時間必須為 O(len(list1) + len(list2))，且不得使用函式庫內建的集合（set）操作。
        """
        result = []
        p1 = 0  # list1 的指標
        p2 = 0  # list2 的指標
        
        len1 = len(list1)
        len2 = len(list2)
        
        while p1 < len1 and p2 < len2:
            doc_id1 = list1[p1]
            doc_id2 = list2[p2]
            
            if doc_id1 == doc_id2:
                # 找到共同的記錄 ID
                result.append(doc_id1)
                p1 += 1
                p2 += 1
            elif doc_id1 < doc_id2:
                # list1 的 ID 較小，移動 p1
                p1 += 1
            else: # doc_id1 > doc_id2
                # list2 的 ID 較小，移動 p2
                p2 += 1
                
        return result

    def process_query(self, keywords: List[str]) -> List[int]:
        """
        處理給定的關鍵字查詢：抓取每個關鍵字對應的倒排列表並計算它們的交集。
        """
        # 1. 處理空查詢
        if not keywords:
            return []
        
        # 將所有關鍵字轉為小寫以進行查找
        normalized_keywords = [k.lower() for k in keywords if k]
        
        if not normalized_keywords:
             return []

        # 2. 獲取第一個關鍵字的倒排列表作為初始交集結果
        first_keyword = normalized_keywords[0]
        if first_keyword not in self.inverted_lists:
            # 如果第一個關鍵字就不存在，則交集為空
            return []
            
        current_intersection = self.inverted_lists[first_keyword]
        
        # 3. 迭代其餘關鍵字並逐步計算交集
        for i in range(1, len(normalized_keywords)):
            keyword = normalized_keywords[i]
            
            # 如果當前交集已經是空的，則無需繼續計算，結果必然是空
            if not current_intersection:
                return []
                
            # 獲取下一個關鍵字的倒排列表
            if keyword in self.inverted_lists:
                next_list = self.inverted_lists[keyword]
                # 使用 intersect 函式計算交集
                current_intersection = self.intersect(current_intersection, next_list)
            else:
                # 如果查詢中任一關鍵字不存在，則最終交集為空
                return []
                
        return current_intersection


def main():
    """
    從給定文字檔建構倒排索引，然後在一個無限迴圈中不斷詢問使用者輸入查詢關鍵字，
    並輸出最多三筆符合條件的記錄（標題與描述）。
    """
    # 1. 解析命令列參數
    if len(sys.argv) != 2:
        print("用法: python3 %s <檔案路徑>" % sys.argv[0])
        sys.exit(1)

    file_name = sys.argv[1]

    # 2. 建立倒排索引
    ii = InvertedIndex()
    ii.build_from_file(file_name)
    
    # 3. 無限查詢迴圈
    while True:
        try:
            # 獲取使用者輸入
            query_string = input("\n請輸入查詢關鍵字（以空格分隔，或按 Ctrl+D/Ctrl+Z 退出）： ").strip()
            
            # 處理空輸入
            if not query_string:
                continue
                
            # 分詞 (Tokenize)
            keywords = query_string.split()
            
            # 處理查詢，取得匹配的記錄 ID 列表
            matching_record_ids = ii.process_query(keywords)
            
            # 4. 輸出結果 (最多三筆)
            
            num_results = len(matching_record_ids)
            print("-" * 30)
            print(f"共找到 {num_results} 筆匹配的記錄。")
            
            # 決定要顯示的筆數
            display_count = min(num_results, 3)
            
            if display_count > 0:
                print(f"顯示前 {display_count} 筆結果 (以記錄 ID 排序):")
                
                # 記錄 ID 列表已經是排序好的，因此前三筆就是最先出現在檔案中的三筆
                for i in range(display_count):
                    record_id = matching_record_ids[i]
                    # 從 self.records 中獲取標題和描述
                    title, description = ii.records[record_id]
                    
                    # 輸出格式
                    print(f"\n--- 結果 {i+1} (記錄 ID: {record_id}) ---")
                    print(f"標題 (Title): {title}")
                    
                    # 描述內容過長時，僅顯示部分片段
                    snippet = description[:100] + ("..." if len(description) > 100 else "")
                    print(f"描述片段 (Snippet): {snippet}")
                    
            print("-" * 30)
            
        except Exception as e:
            print(f"錯誤: {e}")
            break


if __name__ == "__main__":
    main()
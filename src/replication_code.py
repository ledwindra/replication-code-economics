import matplotlib.pyplot as plt
import pandas as pd
import requests

class ReplicationCode:
    
    def __init__(self):
        self.url = 'https://api.github.com/search/repositories?q=replication+code+language%3Astata&type=Repositories&page='
        
    def total_page(self):
        item = 30
        page = 1
        while item < 103:
            page += 1
            item += 30
        
        return page
    
    def result(self):
        page = self.total_page()
        result = []
        i = 0
        while i < page:
            res = requests.get(f'{self.url}{i+1}')
            res = res.json()
            res = res['items']
            result.append(res)
            i += 1
            
        return result
    
    def created_at(self):
        result = self.result()
        
        created_at = []
        for i in result:
            for j in i:
                created_at.append(j['created_at'][:4])
                
        return created_at
    
    def dataframe(self):
        created_at = self.created_at()
        df = pd.DataFrame(created_at, columns=['created_at'])
        df = df.groupby('created_at').size().to_frame().reset_index()
        df = df.rename(columns = {0: 'count'})
        df = df.sort_values(by='created_at', ascending = True)
        
        return df
    
    def plot(self):
        df = self.dataframe()
        fig, ax = plt.subplots(figsize=(15, 5))
        plt.plot('created_at', 'count', data=df)
        plt.grid(b=True)
        plt.title('Public repositories with "replication code" keywords for Stata language')
        plt.xticks(rotation=-45)
        plt.xlabel('Year created')
        plt.ylabel('Total repositories')
        plt.savefig('img/replication-code-stata.png', bbox_inches = 'tight')
        
if __name__ == '__main__':
    rc = ReplicationCode()
    rc.plot()
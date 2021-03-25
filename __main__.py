import pyautogui
from time import sleep

class GeneScanner:
    def __init__(self):
        self.genes = ['X', 'Y', 'G', 'W', 'H']
        self.list = []
    
    def run(self):
        while True:
            self.update()
            sleep(.5)

    def update(self):
        self.current = pyautogui.screenshot(region=(1160, 360, 285, 40))
        self.scanAll()
    
    def searchFor(self, gene):
        matches = []
        lastMatch = -1
        for coords in pyautogui.locateAll("genes/%s.png" % (gene), self.current, confidence=.75):
            if lastMatch > 0 and coords.left - lastMatch < 30: 
                continue
            matches.append((gene, coords.left))
            lastMatch = coords.left
        return matches

    def scanAll(self):
        grab = []
        for gene in self.genes:
            grab += self.searchFor(gene)
        reg = sorted(grab, key=lambda x: x[1])
        if (len(reg) != 6):
            return
        self.add(''.join(i[0] for i in reg))
    
    def add(self, genetic):
        if genetic not in self.list:
            print('New seed :', genetic)
            self.list.append(genetic)
            with open('list.txt', 'w') as fp:
                fp.write('\n'.join('%s' % x for x in self.list))

instance = GeneScanner()
instance.run()
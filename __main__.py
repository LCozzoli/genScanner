import pyautogui
import winsound
import os
from time import sleep

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
        for coords in pyautogui.locateAll(resource_path("./genes/%s.png" % (gene)), self.current, confidence=.75, grayscale=True):
            if any(((coords.left-10) <= match[1] <= (coords.left + 10) ) for match in matches):
                continue
            matches.append((gene, coords.left))
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
            self.list.append(genetic)
            winsound.Beep(440, 200)
            print('New seed #%d:' % (len(self.list)), genetic)
            with open('list.txt', 'w') as fp:
                fp.write('\n'.join('%s' % x for x in self.list))

instance = GeneScanner()
print('Running genScanner by SegFault..\n\nPlease ensure that you\'ve set your resolution to 1920x1080\nAlso check that graphics.uiscale is set to 1\nResult file will output to list.txt\n\nThanks to trausi for the detection fix ♥')
instance.run()
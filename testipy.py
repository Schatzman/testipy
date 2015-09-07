#!/usr/bin/env python3.4
from actor import ActorEngine, worker
from GUI import Window, AppGUI

if __name__ == '__main__':
    main = Window()
    main.auto_configure()
    gui = AppGUI(main)

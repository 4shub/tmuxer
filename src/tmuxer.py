import yaml
import libtmux
import os
import sys


def processWindow(pane_data, current_pane, all_panes):
    next_pane = current_pane
    pane_exists = False

    if pane_data.get('goto'):
        next_pane = all_panes[int(pane_data.get('goto')) - 1]
        pane_exists = True

    if pane_data.get('split'):
        is_vertical = pane_data.get('split') == 'v'
        next_pane = next_pane.split_window(vertical=is_vertical)
        pane_exists = False

    #if pane_data.get('name'):
        #name = pane_data.get('name')
        #next_pane.cmd('printf \'\/033]2;My Title\033\/\/\'')

    if pane_data.get('run'):
        next_pane.send_keys(pane_data.get('run'))

    if pane_data.get('resize'):
        resize = pane_data.get('resize')

        if resize.get('height'):
            next_pane.resize_pane(height=resize.get('height'))

    if pane_exists:
        return False

    return next_pane


def tmuxer():
    currentDirectory = os.getcwd()
    configName = sys.argv[1] if 1 < len(sys.argv) else None
    configURL = ''

    noConfigNameDir = currentDirectory + '/tmuxer.yaml'

    if not configName and os.path.isfile(noConfigNameDir):
        configURL = noConfigNameDir
    elif configName and os.path.exists(os.path.join(os.getcwd(), configName)):
        configURL = configName
    else:
        print("No config specified or no tmuxer.yaml in current directory")
        exit(1)

    bash = "#!/bin/bash\n"
    script = ""
    document = open(configURL, 'r')
    data = yaml.load(document)

    if data.get('run'):
        # run script before launch
        print('meme')

    # start tmux server
    server = libtmux.Server()

    session = server.new_session(session_name="new_session", kill_session=True, attach=False)
    window = session.new_window(attach=True, window_name="new_session")

    panes = []

    last_pane = window.attached_pane
    for pane_data in data.get('windows'):
        current_pane = processWindow(pane_data, last_pane, panes)

        if current_pane:
            last_pane = current_pane
            panes.append(last_pane)


    server.attach_session(target_session="new_session")

if __name__ == '__main__':
    tmuxer()

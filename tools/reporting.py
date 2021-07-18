def save_report():
    with open('log.csv', 'w') as f:
        columns = ['time', 'temperature', 'humidity']
        s = '\t'.join(columns) + '\n'
        f.write(s)


def add_line(l):
    with open('log.csv', 'a') as f:
        columns = ['time', 'temperature', 'humidity']
        s = '\t'.join(l) + '\n'
        f.write(s)
def save_report():
    with open('log.csv', 'w') as f:
        columns = ['time', 'temperature', 'humidity', 'is_active']
        s = '\t'.join(columns) + '\n'
        f.write(s)


def add_line(pars):
    with open('log.csv', 'a') as f:
        s = '\t'.join([str(p) for p in pars]) + '\n'
        f.write(s)
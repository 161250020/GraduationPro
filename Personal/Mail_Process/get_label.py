import shutil

def get_label_in_a_file(original_path, save_path='all_email.txt'):
    f = open(original_path, 'r')
    head1 = "trec06c/trec06c"
    head2 = "trec"
    label_list = []
    len1 = 0
    len2 = 0
    for line in f:
        # spam(垃圾邮件标记为0)
        if line[0] == 's':
            label_list.append('0')
        # ham(普通邮件标记为0)
        elif line[0] == 'h':
            label_list.append('1')
    f = open(save_path, 'w', encoding='utf8')
    f.write('\n'.join(label_list))
    f.close()
if __name__ == "__main__":
    print('Storing labels in a file ...')
    get_label_in_a_file('trec06c/trec06c/full/index', save_path='label.txt')
    print('Store labels finished !')
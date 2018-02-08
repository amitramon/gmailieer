import os
import json


class LabelTranslator:

    gmail_label_sep = '/'
    
    default_remote_to_local_map = {
        'INBOX'     : 'inbox',
        'SPAM'      : 'spam',
        'TRASH'     : 'trash',
        'UNREAD'    : 'unread',
        'STARRED'   : 'flagged',
        'IMPORTANT' : 'important',
        'SENT'      : 'sent',
        'DRAFT'     : 'draft',
        'CHAT'      : 'chat'
    }

    @staticmethod
    def print_info(label_translator=None):
        
        label_map = label_translator.remote_to_local_map if label_translator \
                    else LabelTranslator.default_remote_to_local_map

        print('{0:20} ==> {1:20}'.format('<Remote>', '<Local>'))
        for r,l in label_map.items():
            print('{0:20} ==> {1:20}'.format(r, l))

        label_sep = label_translator.label_separator if label_translator \
                    else 'default'
        
        print('Label separator: {}'.format(label_sep))


        if label_translator:
            if label_translator.has_user_map:
                print("User map loaded")
            else:
                print("No user map loaded, default map will be used")
            if label_translator.label_separator and \
               label_translator.label_separator != '/':
                print("Remote label separator will be replaced with '{}'".format(
                    label_translator.label_separator))
            else:
                print("No user separator, label separator will not be modified")
        else:
            print("Default map will be used, label separator will not be modified")
                
    
    def _update_local_to_remote_map(self):
        self._local_to_remote_map = {v: k for k, v in self._remote_to_local_map.items()}
        
    
    def __init__ (self):

        self._label_separator = None
        self._has_user_map = None
        self._remote_to_local_map = dict(LabelTranslator.default_remote_to_local_map)
        self._update_local_to_remote_map()

    def load_user_translation(self, labels_map_fname):

        with open(labels_map_fname, 'r') as fd:
            user_map = json.load(fd)
            labels_map = user_map.get('labels_map', {})
            if labels_map:
                self._remote_to_local_map.update(labels_map)
                self._has_user_map = True
                
            self._label_separator = user_map.get('label_sep', None)

        self._update_local_to_remote_map()


        
    @property
    def label_separator(self):
        return self._label_separator

    @label_separator.setter
    def label_separator(self, sep):
        self._label_separator = sep

    @property
    def has_user_map(self):
        return self._has_user_map
    
    @property
    def remote_to_local_map(self):
        return self._remote_to_local_map
    
    def local_label_to_remote(self, label):
        """
        Translate local label string to the remote value.
        """
        label = self._local_to_remote_map.get(label, label)
        if self.label_separator:
            label = label.replace(self.label_separator,
                                  LabelTranslator.gmail_label_sep)

        return label
        

    def remote_label_to_local(self, label):
        """
        Translate remote label string to the local value.
        """
        label = self._remote_to_local_map.get(label, label)
        if self.label_separator:
            label = label.replace(LabelTranslator.gmail_label_sep,
                                  self.label_separator)

        return label
            
            
    def local_labels_to_remote(self, labels):

        return [self.local_label_to_remote(label) for label in labels]
        

    def remote_labels_to_local(self, labels):

        return [self.remote_label_to_local(label) for label in labels]



def print_label_translation(label_trans):
    '''Information - list label translation map
    '''
    print('{0:20} ==> {1:20}'.format('<Remote>', '<Local>'))
    for r,l in label_trans.remote_to_local_map.items():
        print('{0:20} ==> {1:20}'.format(r, l))

    print('Label separator: %s' % label_trans.label_separator)
    
def main():

    lt = LabelTranslator()
    print('Default label map')
    print_label_translation(lt)
    
    try:
        labels_file = '/home/amit/test-mail/amitlst/.label-trans.json'
        lt.load_user_translation(labels_file)
    except json.decoder.JSONDecodeError as e:
        print('Bad labels map file ' + labels_file +':')
        print(e)
        exit(1)

    print("")
    print('User label map, read from user\'s file %s' % labels_file)
    print_label_translation(lt)
    print("")
    # for r,l in lt.labels_map.items():
    #     print('{0:10} ==> {1:10}'.format(r, l))

    print("")
    if lt.label_separator:
        print("Sep is valid")
    else:
        print("Sep is None or empty")

    print("")
    if lt.label_separator is None:
        print("None")
    elif len(lt.label_separator) == 0:
        print("Empty")
    else:
        print("Separater: " + lt.label_separator)
        
    # exit(0)
    print("")
    print("Local separator: %s" % lt.label_separator)
    print("")

    local_labels = ['hello', 'world', 'deleted', 'inbox', 'my-local', 'cat1::cat2::cat3']
    remote_labels = lt.local_labels_to_remote(local_labels)
    local_labels2 = lt.remote_labels_to_local(remote_labels)

    print("local labels original values:")
    for l in local_labels:
        print(l)

    print("")
    print("translated to remote values:")
    for l in remote_labels:
        print(l)

    print("")
    print("remote translated back to local values:")
    for l in local_labels2:
        print(l)

    print("")
    mylabel = 'deleted'
    print(mylabel)
    print(lt.local_label_to_remote(mylabel))
    print(mylabel)
        
if __name__ == '__main__':
    main()



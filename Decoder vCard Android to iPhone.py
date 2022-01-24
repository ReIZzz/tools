# join rows & decode vCard File (Visit Card File) *.vcf
# exported from Android for load to iPhone

import codecs


List_contact = []
# n = 20

File = "Контакты.vcf"
with open(File) as file:
    first_rows = file.readlines()   #[:n]
    for i in first_rows:
        List_contact.append(i)


# many very long rows have wraps (that rows started from "="). Function below remove it
def Merger(list_row):
    list_merged = []
    for i in list_row:
        if i[0] == '=':
            list_merged[-1] = (list_merged[-1][:-2] + i[:-1] + '\n')
        else:
            list_merged.append(i)
    return (list_merged)


List_contact_mergered = Merger(List_contact)
file_output = codecs.open('Contact_decode.vcf', 'w', 'utf-8')

for l in List_contact_mergered:
    file_output.write(l)

file_output.close()

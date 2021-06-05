import os
from usps import USPSApi
from sys import platform
from configparser import ConfigParser
from threading import Thread



class Main_app:
    def __init__(self):
        self.clearscreen()
        self.config = ConfigParser()
        self.config.read('config.cfg')

        self.DEFAULT_ID = '9400108205496'
        self.DEFAULT_ID2 = 'RR'

        self.error_list = []
        self.error_str=""
        self.out_list = []
        self.out_text=""
        self.in_text=""
        self.tracking_id = []
        self.id_range()
        self.main()

    def main(self):
        while len(self.tracking_id) == 0:
            print('NO DATA, Press enter to generate from range')
            pressme = input()
            self.clearscreen()
            self.id_range()

        print('DATA processed, Press ENTER KEY to search DATABASE')
        self.pressme = input()
        self.clearscreen()
        zip_data = input('Zip code: XXXXX -> ')
        if len(zip_data) == 0:
            self.zip_data = '23SJDSJDNJED6EFGB3##'
        self.date_data = input('Date: MM DD YYYY  Example(3 MARCH 2021)-> ').split()
        if len(self.date_data) == 3:
            self.date_data = (self.date_data[1] + ' ' + self.date_data[0] + '|' + self.date_data[2])
        else:
            pass
        if len(self.date_data) == 0:
            self.date_data = '23SJDSJDNJED6EFGB3##'
        delivery = input('''Delivery:-
          In transit = 1
          Collecting = 2
          Delivered  = 3

        Choise(1/2/3):-''')
        if delivery == 1:
            self.delivery = 'Arrived at'
        elif delivery == 2:
            self.delivery = 'Collecting'
        elif delivery == 3:
            self.delivery = 'Out for Delivery'
        else:
            self.delivery = ' '

        files = os.listdir('Data')
        w = 0
        file_name = input('File Name:- ')
        if file_name == '':
            file_name = 'DEFAULT_NAME'
        else:
            pass
        file_open_track = open(file_name + '.txt', "a+")
        while w < len(files):
            tracking_num_data = str(files[w])
            file = open('Data/' + tracking_num_data).read()
            self.check(file, tracking_num_data, file_name, file_open_track)
            w += 1
        file_open_track.close()

        file_open_track_del = open(file_name + '.txt', 'r')
        file_open_track_del = file_open_track_del.read()

        if len(file_open_track_del) == 0:
            self.remove(file_name + '.txt')

    def remove(self,file):
        if os.path.exists(file):
            os.remove(file)

    def check(self,file_data, tracking_num_data, file_name, file_open_track):
        # global zip_data, date_data, delivery
        if ((self.zip_data in file_data) and (self.date_data in file_data) and (self.delivery in file_data)):
            result = 'The tracking ID is:-' + tracking_num_data.replace(".txt", "")
            print(result)
            file_open_track.write(result + '\n')
        elif ((self.zip_data in file_data) or (self.delivery in file_data) or (self.date_data in file_data)):
            result = 'General Data:-' + tracking_num_data.replace(".txt", "")
            print(result)
            file_open_track.write(result + '\n')
        else:
            pass


    def clearscreen(self):
        if platform == "linux" or platform == "linux2":
            os.system("clear")
        elif platform == "win32":
            os.system("cls")

    def invalid_id_confirm(self,id, usps):
        try:
            if str(id) in open('Invalid_ID.txt').read():
                pass
            else:
                self.track(id, usps)
        except:
            self.track(id, usps)

    def track(self,id, usps):
        track = usps.track(id)
        track = track.result
        track = track['TrackResponse']
        track = track['TrackInfo']

        try:
            track = track['TrackDetail']
        except:
            pass

        track = str(track).replace("[{", "").replace("{", "Q1P2W3O4EIRYRY").replace("}", "").replace("]", "")
        # file_open_out = open("out.txt", "a+")
        # file_open_out.write(track)
        # file_open_out.close()
        self.out_text+=track + "\n"
        if 'Error' in track:
            print("Tracking ID:- "+id+' Is Invalid')
            # ferror = open("Invalid_ID.txt", "a")
            # ferror.write('\n'+id)
            # ferror.close()
            # self.error_str+="Tracking ID:- "+id+' Is Invalid'+"\n"
            self.error_list.append(id)
        else:
            self.out_list.append(id)
            self.in_text+=self.out_text.replace('Q1P2W3O4EIRYRY', '\n\n').replace(", ", "|") + "\n"
            # fin = open("out.txt", "rt")
            # fout = open('Data/'+id+".txt", "wt")
            # for line in fin:
            #     fout.write(line.replace('Q1P2W3O4EIRYRY', '\n\n').replace(", ", "|"))
            # fin.close()
            # fout.close()
            print("Tracking ID:- " + id + ' processed successfully')
        # remove('out.txt')

    def thread_process(self,range_data, n):
        # print(range_data)
        # print(n)
        while n <= int(range_data):
            track_num = (self.DEFAULT_ID + str(n).zfill(9))  # 9400108205496[XXXXXXX]
            track_num2 = (self.DEFAULT_ID2 + str(n).zfill(9) + 'US')  # RA[XXXXXXX]US
            # with open('track.txt', 'r+') as exist:
            #   line2 = exist.read()
            if track_num2 and track_num in self.tracking_id:
                pass
            else:
                self.tracking_id.append(track_num)
                self.tracking_id.append(track_num2)
            n += 1

    def id_range(self):
        range_data = input('Range from ' + self.DEFAULT_ID + '000000000' + ' to:- ')
        if len(range_data) == 9:
            if range_data.isnumeric():
                # n = 0
                range_data = int(range_data)
                div_4_status = True
                var = 0
                if int(range_data) % 8 != 0:
                    range_data = range_data - (range_data % 8)
                    var = (range_data % 8)
                # while n <= int(range_data):
                # print(n)


            else:
                print('Enter only numberes!!')
                self.id_range()
        elif len(range_data) == 0:
            pass
        else:
            print('Enter 9 Digits!!')
            self.id_range()

        textfile = open("track.txt", "w")
        for element in self.tracking_id:
            textfile.write(element + "\n")
        textfile.close()
        print("data added to text file")
        # d=0
        # with open('track.txt', 'r') as filehandle:
        #     for line in filehandle:
        #       currenttracking_id = line.replace("\n", "")
        #       print(currenttracking_id)
        #       d+=1
        #       if d==3:
        #         exit()
        #       tracking_id.append(currenttracking_id)

        self.API_switch_DEF(0)

    def validate_thread(self, userId, id_list, start, end):
        API_switch = 0
        for q in range(start, end):
            tracking_num = str(id_list[q])
            try:
                usps = USPSApi(userId[API_switch])
                self.invalid_id_confirm(tracking_num, usps)
            except:
                print('API ERROR:- ' + userId[0])
                API_switch = 1
                try:
                    usps = USPSApi(userId[API_switch])
                    self.invalid_id_confirm(tracking_num, usps)
                except:
                    print('API ERROR:- ' + userId[API_switch])
                    API_switch += 1
                    self.API_switch_DEF(API_switch)

    def API_switch_DEF(self,API_switch):
        q = 0
        userId = self.config['TRACK']['key'].split(',')
        total_numbers = len(self.tracking_id)
        var = 0
        if len(self.tracking_id) % 4 != 0:
            var = len(self.tracking_id) % 4
            total_numbers = total_numbers - var

        thread1 = Thread(target=self.validate_thread, args=(userId, self.tracking_id, 0, total_numbers // 4), )
        thread2 = Thread(target=self.validate_thread,
                         args=(userId, self.tracking_id, total_numbers // 4, (2 * total_numbers) // 4), )
        thread3 = Thread(target=self.validate_thread,
                         args=(userId, self.tracking_id, (2 * total_numbers) // 4, (3 * total_numbers) // 4), )
        thread4 = Thread(target=self.validate_thread,
                         args=(userId, self.tracking_id, (3 * total_numbers) // 4, total_numbers + var), )
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()


main_app_obj=Main_app()
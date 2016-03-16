import json
import sqlite3


def insert_to_sql(json_file):
    db = sqlite3.connect('runlog.db')
    traffic = json.load(open(json_file))

    amp_avg = traffic["Amp_Avg"]
    curr = traffic["Current"]
    date = traffic["Datetime"]
    gain = traffic["Gain"]
    run_no = traffic["Run_No"]
    serial_no = traffic["Serial_No"]
    subrun_no = traffic["Subrun_No"]
    temp = traffic["Temperature"]
    run_type = traffic["Type"]
    volt = traffic["Voltage"]

    data = [amp_avg, curr, date, gain, run_no, serial_no,
            subrun_no, temp, run_type,  volt]

    c = db.cursor()
    string = 'amp_avg, curr, date, gain, run_no, ' \
             'serial_no, subrun_no, temp, run_type, volt'
    c.execute('create table runlog ({})'.format(string))
    c.execute('insert into runlog values (?,?,?,?,?,?,?,?,?,?)', data)
    db.commit()
    c.close()

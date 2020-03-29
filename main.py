import argparse
import datetime
from pdf2dicom import generate_dicom_from_pdf

def generate_random_uid():
    return '1.9.9.' + str(datetime.datetime.now().strftime('%H%M%S%f%d%m%Y'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_pdf', type=str, help='Input PDF to convert to DICOM')
    args = parser.parse_args()
    input_pdf = args.input_pdf
    e_pdf_ds = generate_dicom_from_pdf(input_pdf)
    e_pdf_ds.Modality = 'CR'

    e_pdf_ds.PatientName = 'John Doe'
    e_pdf_ds.PatientID = '12345'
    e_pdf_ds.PatientSex = 'M'
    e_pdf_ds.StudyInstanceUID = generate_random_uid()

    e_pdf_ds.SeriesInstanceUID = generate_random_uid()
    e_pdf_ds.SOPInstanceUID = generate_random_uid() 

    e_pdf_ds.save_as('converted_dicom.dcm')

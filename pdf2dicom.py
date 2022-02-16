import pydicom
import tempfile
import datetime
from pydicom.dataset import Dataset, FileDataset

def generate_dicom_from_pdf(pdf_file):
    suffix = '.dcm'
    filename = tempfile.NamedTemporaryFile(suffix=suffix).name

    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.104.1'
    file_meta.MediaStorageSOPInstanceUID = '2.16.840.1.114430.287196081618142314176776725491661159509.60.1'
    file_meta.ImplementationClassUID = '1.3.46.670589.50.1.8.0'
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'

    ds = FileDataset(filename, {},
                 file_meta=file_meta, preamble=b"\0" * 128)

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    timeStr = dt.strftime('%H%M%S.%f')
    ds.ContentTime = timeStr

    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.104.1'

    with open(pdf_file, 'rb') as f:
        f_read = f.read()
        ValueLength = len(f_read)
        ## All Dicom Element must have an even ValueLength
        if ValueLength % 2 != 0:
            f_read += b'\0'
        ds.EncapsulatedDocument = f_read

    ds.MIMETypeOfEncapsulatedDocument = 'application/pdf'

    ds.Modality = 'DOC' #document
    ds.ConversionType = 'WSD' #workstation
    ds.SpecificCharacterSet = 'ISO_IR 100' 
    # more codes for charecter encoding here https://dicom.innolitics.com/ciods/cr-image/sop-common/00080005 

    return ds

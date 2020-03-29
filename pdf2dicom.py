import pydicom
import tempfile
import datetime
from pydicom.dataset import Dataset, FileDataset

def generate_dicom_from_pdf(pdf_file):
    suffix = '.dcm'
    filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name

    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.104.1'
    file_meta.MediaStorageSOPInstanceUID = '2.16.840.1.114430.287196081618142314176776725491661159509.60.1'
    file_meta.ImplementationClassUID = '1.3.46.670589.50.1.8.0'

    ds = FileDataset(filename_little_endian, {},
                 file_meta=file_meta, preamble=b"\0" * 128)

    ds.is_little_endian = True
    ds.is_implicit_VR = True

    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    timeStr = dt.strftime('%H%M%S.%f')
    ds.ContentTime = timeStr

    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.104.1'

    with open(pdf_file, 'rb') as f:
        ds.EncapsulatedDocument = f.read()

    ds.MIMETypeOfEncapsulatedDocument = 'application/pdf'

    return ds

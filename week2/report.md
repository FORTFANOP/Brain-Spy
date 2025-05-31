# Week2: MRI Data Visualization Report

**Assignment:** Week 2 - MRI Visualization using NIfTI and DICOM

Joel John Mathew, 240499

---

## Objective

To load, process, and visualize 3D MRI data from NIfTI (`.nii`) and DICOM (`.dcm`) formats using Python, `nibabel` and `pydicom`. The aim is to extract metadata, construct 3D volumes, visualize standard anatomical planes, and compare both formats in terms of structure and usability.

---

## Data Used

- **NIfTI Data:** Provided in repo (`sample_data/...nii`)
- **DICOM Data:** Downloaded from Kaggle [Brain MRI Scans](https://www.kaggle.com/datasets/trainingdatapro/dicom-brain-dataset)
  - Series used: `SE000002` (125 slices)

---

## Approach

### 1. **Loading NIfTI Data**
  First, I loaded `.nii` file using `nibabel`
  ```
  path = '.\sample_data\data_name.nii'
  img = nib.load(path)
  data = img.get_fdata()
  ```
  Then I extracted some general data, such as the image shape, affine matrix, etc.
  Shape: `(256, 362, 384)`

  I also plotted some images of the different planes (See visualisation section)

### 2. **DICOM Data**
  I also loaded in the DICOM data using `pydicom`.
  ```
  path = '.\sample_data\dicom_data\SE000002'  # I'm using only the folder that has the most .dcm files in it

  files = os.listdir(path)    # contains both .jpg and .dcm files

  slices = [pydicom.dcmread(os.path.join(path, file)) for file in files if file.endswith('.dcm')]
  ```
  I used the SE000002 folder only because the other folders had way too less slices (ex, SE000001 had only 9 slices) and they were giving very distorted image when I tried to visualise them.

  The current data too has disproportionate shape, and during plotting was giving distorted and broken figure (why is this??)

  Further, I stacked all the DICOM slices to obtain a volume of shape (288, 288, 125)
  ```
  volume = []

  for slice in slices:
    volume.append(slice.pixel_array)

  volume = np.array(volume)
  volume.shape    # currently: (125, 288, 288)

  # converting to (saggital, coronal, axial)
  volume = np.transpose(volume, (2, 1, 0))
  ```

  I also extracted some metadata:
  ```
  # checking metadata for one slice
  sample_slice = slices[0]
  print(sample_slice.Modality)   # 'MR' signifies MRI scan
  print(sample_slice.PatientName)
  print(sample_slice.InstanceNumber)  # order of the slice wrt all the slices
  print(sample_slice.SliceThickness)  # in mm
  ```

- Extracted metadata:
  - PatientName: Anonymous (Usually is the case for public datasets)
  - Modality: MR
  - Instance: 4
  - Slice Thickness: 5 mm

### 3. **Visualization**
I used matplotlib to display:
- Axial, Coronal, Sagittal views of DICOM and NIfTI data
- Interactive slider using `ipywidgets`
- Created animation of slices and saved as `.gif`


#### **NIfTI Slices**  

<img src=".\imgs\nifti_slices.png" alt="nii" width="600" height="200">

#### **DICOM Slices**  
This one has some issues, due to discrepency in the number of slices, the image appears cropped. Further, it appears broken with lines across (not sure why)

<img src=".\imgs\dicom_slices.png" alt="dcm" width="600" height="200">

#### **Slider**  

<img src=".\imgs\slider.gif" alt="slider" width="350" height="350">

### **Animated GIFs**
<img src=".\imgs\nii_ani_axi.gif" alt="gif_preview" width="300" height="250">

<img src=".\imgs\nii_ani_cor.gif" alt="gif_preview" width="300" height="250">

<img src=".\imgs\nii_ani_sag.gif" alt="gif_preview" width="300" height="250">

---


## Observations

- NIfTI files are easier to use and manage for us, since it has limited patient metadata and the full volume is stored as a single file.
- DICOM is more oriented towards medical field, as it has separate metadata about the patient, type of scan, etc. Also is inconvenient since we have to load each slice separately to make the volume

---

## Problems

- The interactive widgets part was confusing and getting them to work together required additional _help_ (🥲)
- The DICOM files don't seem to be correct due to the very visible breaks in the slices. Not sure if the data itself is that way or some other mistake


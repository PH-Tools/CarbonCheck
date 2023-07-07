---
title: "Baselines"
weight: 20
---
# Creating Baseline Models
CarbonCheck includes tools to create automatic baseline versions of your PHPP or WUFI-Passive energy models. These features allow you to specify a 'source' model which describes your proposed design, and then CarbonCheck will modify this model to match the requirements of the New York State Energy Conservation Code baseline configuration. The exact baseline specifications used will vary depending on the climate zone and other building attributes. For more information on the baseline settings required, see the [NYS Energy Code | Section C407.5.1](https://up.codes/viewer/new_york/ny-energy-conservation-code-2020/chapter/CE_4/ce-commercial-energy-efficiency#C407.5.1)


The basic usage steps for both WUFI-Passive and PHPP are shown below.

## 1. WUFI Baselines

### Step 1a. Save your model as an XML File
To get started, you will need a valid WUFI-Passive model with your proposed building design. In order to let CarbonCheck read in this model data, first export your WUFI-Model as an xml file, and save the file to your computer someplace that you will be able to find it.
![Basic honeybee-model grasshopper](/CarbonCheck/img/baseline/WUFI_save_as_XML_1.png)
![Basic honeybee-model grasshopper](/CarbonCheck/img/baseline/WUFI_save_as_XML_2.png)

### Step 1b. Read in the XML File
Open up CarbonCheck and navigate to the 'Create Baseline Model' tab, if it is not already open. At the top, you will see an option to specify the source file. This WUFI-XML file is the 'source' file you want CabonCheck to read in. Simply navigate to the folder where you save the XML file, and select it.
![Basic honeybee-model preview](/CarbonCheck/img/baseline/WUFI_specify_xml.png)

### Step 1c. Specify the Baseline Configuration
Using the options in the dropdown menus, select the appropriate configuration settins for your project's climate zone and type. For questions on the correct options to specify for your prject, take a look at the [NYS Energy Code | Section C407.5.1](https://up.codes/viewer/new_york/ny-energy-conservation-code-2020/chapter/CE_4/ce-commercial-energy-efficiency#C407.5.1)
![Basic honeybee-model preview](/CarbonCheck/img/baseline/WUFI_options.png)

### Step 1d. Create the Baseline Model
Once the source model and options are specified, generate the baseline model. CarbonCheck will read in the XML file, modify attributes such as window U-Valus and wall R-Values in line with the baseline configurations specified, and then save out a brand new WUFI-XML file.
![Basic honeybee-model preview](/CarbonCheck/img/baseline/WUFI_run.png)


### Step 1e. Open the new WUFI-Baseline Model
Using WUFI-Passive, open the newly generated XML file as you would any other WUFI-Passive file. Once it opens, you will see that the specifications for the project have been adjusted to match the code-required baseline levels throughought.
![Basic honeybee-model preview](/CarbonCheck/img/baseline/WUFI_open_xml_1.png)
Note: if you don't see your new baseline file at first, be sure to select 'XML' from the Open dialog window's filter.
![Basic honeybee-model preview](/CarbonCheck/img/baseline/WUFI_open_xml_2.png)

Success. You now have a properly baseline'd energy model you can use for comparing your proposed design to.

## 2. PHPP Baselines

### Step 2a. Specify the 'Source' PHPP File
Using CarbonCheck, specify the 'source' PHPP file which describes your proposed design. It is best practice to make a backup copy of this PHPP file before proceeding to ensure that CarbonCheck doesn't overwrite anything critical to your design model. If this file is not already open, CarbonCheck should open this file using Microsoft Excel automatically.
![Basic honeybee-model preview](/CarbonCheck/img/baseline/PHPP_specify_phpp.png)

### Step 2b. Specify the Baseline Configuration
Using the options in the dropdown menus, select the appropriate configuration settins for your project's climate zone and type. For questions on the correct options to specify for your prject, take a look at the [NYS Energy Code | Section C407.5.1](https://up.codes/viewer/new_york/ny-energy-conservation-code-2020/chapter/CE_4/ce-commercial-energy-efficiency#C407.5.1)
![Basic honeybee-model preview](/CarbonCheck/img/baseline/WUFI_options.png)

### Step 2c. Create the Baseline Model
Once the source model and options are specified, generate the baseline model. CarbonCheck will walk through the PHPP file, modifying attributes such as window U-Valus and wall R-Values in line with the baseline configurations specified. Once this is complete, you an save or save-as the PHPP file to your hard drive.
![Basic honeybee-model preview](/CarbonCheck/img/baseline/WUFI_run.png)

Success. You now have a properly baseline'd energy model you can use for comparing your proposed design to.
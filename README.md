# NLCC for Local Pseudopotentials

This repository provides tools and workflows for incorporating **Non-Linear Core Corrections (NLCC)** into **local pseudopotentials**. Two distinct methodologies are presented for constructing the NLCC contribution, each implemented through interactive Jupyter notebooks.

## Methods of NLCC Construction

### 1. Gaussian-Based NLCC
- **Notebook:** `NLCC_Gaussian.ipynb`
- **Description:**  
  A simple Gaussian core charge density is constructed and embedded directly into a `psp8` formatted pseudopotential file. This method allows for a quick and analytical way to introduce an NLCC profile.

### 2. All-Electron (AE) Density-Based NLCC
- **Notebook 1:** `NLCC_AE_strength.ipynb`  
- **Notebook 2:** `NLCC_AE.ipynb`  
- **Description:**  
  The AE-based approach builds the NLCC using the actual all-electron core density. An initial study of the NLCC **strength** derived from the AE density is performed in the first notebook. Once the appropriate strength is identified, a deeper and more refined NLCC analysis is conducted in the second notebook.


## Calculator Discrepancy 

### Notebook: `TEST_DFTpyCalculator.ipynb`
- This notebook investigates inconsistencies in energy curves produced by the modified DFTpy calculator.
- It demonstrates that the **energy curves do not match** those obtained from the standard DFTpy approach, as previously shown in `NLCC_AE_strength.ipynb`.


## Notebooks Summary

| Notebook Name               | Purpose                                                                 |
|-----------------------------|-------------------------------------------------------------------------|
| `NLCC_Gaussian.ipynb`       | Build and export a Gaussian-based NLCC to a psp8 file                   |
| `NLCC_AE_strength.ipynb`    | Analyze and select appropriate NLCC strength from AE density            |
| `NLCC_AE.ipynb`             | Perform detailed AE-based NLCC analysis                                 |
| `TEST_DFTpyCalculator.ipynb`| Compare modified vs standard DFTpy energy curves                        |


## Requirements
To run the notebooks, make sure to install the lpps branch from dftpy as well as PStudio for the AE data.


### Pre-Trained Models

Megaseg

Megaseg-lite

| Category           | Name              | MegaSeg_v1                                                                                  | MegaSeg_light                                                          |
|--------------------|-------------------|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| **Model Properties**   | Description       | CNN-based segmentation model trained on 2600 open 3D fluorescent microscopy images of cellular structures in human hiPSCs | Lighter version of MegaSeg which compromises accuracy for speed       |
|                    | Architecture       | nnUNet                                                                                      | small nnUNet with fewer kernels                                       |
|                    | Loss Function      | Generalized dice focal loss                                                                 | Generalized dice focal loss                                           |
|                    | Optimization       | Adam                                                                                        | Adam                                                                  |
|                    | # of Epochs        | 1000                                                                                        | 1000                                                                  |
|                    | Stopping Criteria  | Validation loss not improving for 100 epochs                                               | Validation loss not improving for 100 epochs                          |
|                    | System Trained On  | Nvidia A100                                                                                | Nvidia A100                                                           |
|                    | Validation Step    | -                                                                                          | -                                                                     |
| **Dependencies**   | CytoDL Version     | 1.7.1                                                                                       | 1.7.1                                                                 |
|                    | PyTorch Version    | 2.4.0+cu118                                                                                | 2.4.0+cu118                                                           |
| **Training Data**  | Image Resolution   | 55x624x924; 60x624x924; 65x600x900; 65x624x924; 70x624x924; 75x624x924; 75x600x900         | 55x624x924; 60x624x924; 65x600x900; 65x624x924; 70x624x924; 75x624x924; 75x600x900 |
|                    | Minimum Image Size | -                                                                                          | -                                                                     |
|                    | Microscope Objective | 100x                                                                                    | 100x                                                                  |
|                    | Microscopy Technique | Spinning disk confocal                                                                    | Spinning disk confocal                                                |
|                    | Public Data Link   | [Dataset Link](https://open.quiltdata.com/b/allencell/tree/aics/hipsc_single_cell_image_dataset/) | [Dataset Link](https://open.quiltdata.com/b/allencell/tree/aics/hipsc_single_cell_image_dataset/) |
|                    | Expected Performance | On NVIDIA-A100, 80GB, Inference @ 6.01 Secs for an Input image of size 924x624x65        | On NVIDIA-A100, 80GB, Inference @ 2.32 Secs for an Input image of size 924x624x65 |
|                    | Structures Trained On | Actin bundles, ER(SERCA2), Adherens junctions, Desmosomes, Gap junctions, Myosin, Nuclear pores, Endosomes, ER (SEC61 Beta), Nuclear speckles, Golgi, Tight junctions, Mitochondria | Actin bundles, ER(SERCA2), Adherens junctions, Desmosomes, Gap junctions, Myosin, Nuclear pores, Endosomes, ER (SEC61 Beta), Nuclear speckles, Golgi, Tight junctions, Mitochondria |
| **Inference Data** | Minimum Image Dimension | 16x16x16                                                                            | 16x16x16                                                              |
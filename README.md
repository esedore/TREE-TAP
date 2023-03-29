# TREE TAP
The goal is to write a classifier based on daily pulls on real-time malicious network data which aids in the process of real-time deep packet inspection.

Just random forest classification - made with maple 🍁

                                                                         &&& &&  & &&
                                                                          && &\/&\|& ()|/ @, &&
                                                                          &\/(/&/&||/& /_/)_&/_&
                                                                       &() &\/&|()|/&\/ '%" & ()
                                                                      &_\_&&_\ |& |&&/&__%_/_& &&
                                                                    &&   && & &| &| /& & % ()& /&&
                                                                     ()&_---()&\&\|&&-&&--%---()~
                                                                         &&     \|||
                                                                                 ||==~
                                                                            🍂    |||--🪣
                                                                                 ||| 
                                                                           , -=-~  .-^- 🥞 _
                                                                         `

# Live Capture Analysis (Windows Only)
1) Run DPI_Gauss.py
2) Select Network Interface
3) Check anomaly.log for abnormal packet sizes
W.I.P

# Dataset Classification
1) Run class.py
2) Use peristed PKL classifier model or Apache Parquet model

Currently using the [CIC-IDS-2018](https://www.unb.ca/cic/datasets/ids-2018.html) dataset to train the model

# ELK Stack Integration
W.I.P

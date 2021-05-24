# Video Analyst
This is the implementation of a series of basic algorithms which is useful for video understanding, including Single Object Tracking (SOT), Video Object Segmentation (VOS), etc.

Current implementation list:
* SOT
    * [SiamFC++: Towards Robust and Accurate Visual Tracking with Target Estimation Guidelines](https://arxiv.org/abs/1911.06188) 


## Quick start
### Setup
Please refer to [SETUP.md](docs/SETUP.md)

### Test on VOT
```
python3 ./main/test.py --config 'experiments/siamfc++/siamfcpp_googlenet.yaml'
```
Check out the corresponding _exp_save_ path in _.yaml_ for result and raw result data, both named by _exp_name_ in _.yaml_.

#### Test all experiments
```
bash ./tools/test_VOT.sh
```

## Repository structure (in progress)
```
├── experiments  # experiment configurations, in yaml format
├── main
│   ├── train.py  # trainng entry point
│   └── test.py  # test entry point
├── video_analyst
│   ├── data  # modules related to data
│   │   ├── dataset  # data fetcher of each individual dataset
│   │   ├── sampler  # data sampler, including inner-dataset and intra-dataset sampling procedure
│   │   ├── dataloader.py  # data loading procedure
│   │   └── transformer  # data augmentation
│   ├── engine  # procedure controller, including traiing control / hp&model loading
│   │   ├── hook  # hook for tasks during training, including visualization / logging / benchmarking
│   │   ├── trainer.py  # train a epoch
│   │   ├── tester.py  # test a model on a benchmark
│   ├── model # model builder
│   │   ├── backbone  # backbone network builder
│   │   ├── common_opr  # shared operator (e.g. cross-correlation)
│   │   ├── task_model  # holistic model builder
│   │   ├── task_head  # head network builder
│   │   └── loss  # loss builder
│   ├── pipeline  # pipeline builder (tracking / vos)
│   │   ├── segmenter  # segmenter builder for vos
│   │   ├── tracker  # tracker builder for tracking
│   │   └── utils  # pipeline utils
│   ├── config  # configuration manager
│   ├── evaluation  # benchmark
│   ├── optimize # optimization-related module (learning rate, gradient clipping, etc.)
│   │   ├── lr_schedule # learning rate scheduler
│   │   ├── optimizer # optimizer
│   │   └── grad_modifier # gradient-related operation (parameter freezing)
│   └── utils  # useful tools
└── README.md
```

## Model ZOO
Please refer to [MODEL_ZOO.md](docs/MODEL_ZOO.md)

## TODO
* [] Training code
* [] Test code for OTB, GOT-10k, LaSOT, TrackingNet

## Acknowledgement
* video_analyst/evaluation/vot_benchmark and other related code have been borrowed from [PySOT](https://github.com/STVIR/pysot)
* video_analyst/evaluation/got_benchmark and other related code have been borrowed from [got-toolkit](https://github.com/got-10k/toolkit.git)

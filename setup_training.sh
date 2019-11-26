#!/bin/bash


ontonotes_path=$1
#data_dir=kor_data
data_dir=data

dlx() {
  wget -P $data_dir $1/$2
  tar -xvzf $data_dir/$2 -C $data_dir
  rm $data_dir/$2
}

download_bert(){
  model=$1
  wget -P models https://storage.googleapis.com/bert_models/2018_10_18/$model.zip
  unzip models/$model.zip
  rm models/$model.zip
  mv $model models/
}

download_spanbert(){
  model=$1
  wget -P models https://dl.fbaipublicfiles.com/fairseq/models/$model.tar.gz
  mkdir models/$model
  tar xvfz models/$model.tar.gz -C models/$model
  rm models/$model.tar.gz
}


conll_url=http://conll.cemantix.org/2012/download
#dlx $conll_url conll-2012-train.v4.tar.gz
#dlx $conll_url conll-2012-development.v4.tar.gz
#dlx $conll_url/test conll-2012-test-key.tar.gz
#dlx $conll_url/test conll-2012-test-official.v9.tar.gz

#dlx $conll_url conll-2012-scripts.v3.tar.gz
#dlx http://conll.cemantix.org/download reference-coreference-scorers.v8.01.tar.gz



vocab_file=models/cased_L-12_H-768_A-12/vocab.txt
#vocab_file=models/multi_cased_L-12_H-768_A-12/vocab.txt

python minimize.py $vocab_file $data_dir $data_dir false

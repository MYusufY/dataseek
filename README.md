# DataSeek

Dataset miner and manager, which uses Selenium DeepSeek automation.

# why?

Datasets are one of the most important factors for LM (language model) development.

A dataset with perfect examples and size makes a perfect LM. Not too much, not too short; it should fit to models size / parameter count.

Making language models can be seem so hard. But in fact, they are just math, trained by your dataset. Hard things are:
- Computational power to train them
- Creating a perfect dataset

Yes, creating a dataset manually would take years. So this is why DataSeek exists.

# demo & guide

## video

Demo video coming soon.

## how to use?

### from source

1. Clone the repository
	``` bash
	git clone https://github.com/MYusufY/dataseek.git
	cd dataseek
	```
2. Lauch it
	``` bash
	pip install -r requirements.txt
	python3 main.py
	```
3. Enter your system prompt
	- A system prompt for DataSeek is the way to describe what kind of dataset you want to be generated to DeepSeek.
	- You should give information about your desired output count per interval, output format, style etc.
	- You can see some examples in the [examples](/examples) folder.

4. Enter your example base JSON dataset (optional)
	- If you enter or import a JSON dataset which already exists, its last 30 examples will be sent to DeepSeek right after the system prompt. So it would have more idea about the format & dataset.
	- This slightly improves performance. You can give a few examples, or a whole dataset to improve it. (not start from scratch- add the new examples on top of it.)
	- Its completely optional.

###  from releases

DataSeek will be released as a standalone app soon, for Linux, macOS and (maybe) Windows. If you want to, you can open an issue to make this process faster!

# Disclaimer

This repository is **only for research purposes**. I am not responsible for misuse. Please do not use in production!

# Contact & Support

📧 [yusuf@tachion.tech](mailto:yusuf@tachion.tech)  
☕ [Buy me a coffee](https://buymeacoffee.com/myusuf)

Thanks — hope this helps!

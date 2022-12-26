sudo rm /usr/bin/mango
sudo rm -rf /usr/local/lib/mango
sudo mkdir /usr/local/lib/mango
sudo cp -r * /usr/local/lib/mango
sudo chmod +x /usr/local/lib/mango/mango.py
sudo ln -s /usr/local/lib/mango/mango.py /usr/bin/mango

rm -rf ~/.mango
mkdir ~/.mango
cd ~/.mango
git clone git@github.com:MathiDEV/mangodb.git

echo "Mongo installed successfully!"
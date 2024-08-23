#!/bin/sh

git clone -b magento-2.3 https://github.com/Mage2Gen/Mage2Gen.git mage2gen-core/magento2.3
git clone -b magento-2.4 https://github.com/Mage2Gen/Mage2Gen.git mage2gen-core/magento2.4

ln -s ./mage2gen-core/magento2.3/mage2gen ./mage2gen3
ln -s ./mage2gen-core/magento2.4/mage2gen ./mage2gen4

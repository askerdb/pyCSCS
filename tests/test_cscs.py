import unittest
import os, sys
sys.path.insert(0, "../")
from pyCSCS import read_bucket, read_css, cscs


class CSCStest(unittest.TestCase):

    def setUp(self):
        self.basepath = os.path.split(os.path.abspath(__file__))[0] + '/'
        self.sample_names, self.featureids, self.features = read_bucket(self.basepath + "data/small_GNPS_buckettable.tsv", normalization = True)
        self.observationids = {str(x):index for index, x in enumerate(self.featureids)}
        self.css = read_css(self.basepath + "data/small_GNPS_edges.tsv", self.observationids, self.features.shape[0], 0.6)

        
    def test_read_bucket_sample_names(self):
        self.assertEqual(self.sample_names, ['Sample1', 'Sample2', 'Sample3', 'Sample4', 'Sample5', 'Sample6'])

    def test_read_bucket_featureids(self):
        self.assertEqual(self.featureids, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_read_bucket_normalized_sum(self):
        self.assertEqual(self.features.sum().sum(), 6)

    def test_read_bucket_unnormalized_sum(self):
        sample_names, featureids, features = read_bucket(self.basepath + "data/small_GNPS_buckettable.tsv", normalization = False)
        self.assertEqual(features.sum().sum(), 3470686603)

    def test_read_css(self):
        self.assertAlmostEqual(round(self.css.sum()),19)

    def test_cscs_1_cpu(self):
        dist = cscs(self.features, self.css, self.sample_names, cpus=1)
        self.assertAlmostEqual(dist.sum().sum(), 25.14, delta=0.01)
        
    def	test_cscs_2_cpu(self):
        dist = cscs(self.features, self.css, self.sample_names, cpus=2)
        self.assertAlmostEqual(dist.sum().sum(), 25.14, delta=0.01)
        
if __name__ == '__main__':
    unittest.main()

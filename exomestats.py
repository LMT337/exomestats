import os
import csv
import glob
import argparse
parser = argparse.ArgumentParser()

parser.add_argument( "infile", type=str )
parser.add_argument( "outfile", type=str )
args = parser.parse_args()

metrics = [
    'qc_dir',
'unique_on_target_aligned_bp',
    'duplicate_on_target_aligned_bp',
    'unique_off_target_aligned_bp',
    'duplicate_off_target_aligned_bp',
    'total_unaligned_bp',
    'total_bp',
    'unique_on_target_aligned_bp_percent',
    'duplicate_on_target_aligned_bp_percent',
    'unique_off_target_aligned_bp_percent',
    'duplicate_off_target_aligned_bp_percent',
    'total_unaligned_bp_percent',
    '20X',
    'mean_depth'
]

infields = [
    'name',
    'id',
    'last_succeeded_build.merged_alignment_result.bam_file'
]

metrics_out = {}

exomeoutfile = args.outfile + '.exomestats.tsv'

with open(args.infile) as csvfile, open(exomeoutfile, 'w') as outfile:

    header_fields = infields + metrics
    reader = csv.DictReader(csvfile, delimiter="\t")
    w = csv.DictWriter(outfile, header_fields, delimiter="\t")
    w.writeheader()

    for line in reader:
        path = line['last_succeeded_build.data_directory'] + '/reference_coverage'
        metrics_out['name'] = line['name']
        metrics_out['id'] = line['id']
        metrics_out['last_succeeded_build.merged_alignment_result.bam_file'] = line['last_succeeded_build.merged_alignment_result.bam_file']
        if os.path.exists(path):
            match = line['last_succeeded_build.data_directory'] + '/reference_coverage' + '/*-wingspan_0-alignment_summary-v2.tsv'
            if glob.glob(match):
                for metrics_file in glob.glob(match):
                    with open(metrics_file) as metcsv:
                        read = csv.DictReader(metcsv, delimiter="\t")
                        for metric in read:
                            metrics_out['qc_dir'] = metrics_file
                            metrics_out['total_bp'] = metric['total_bp']
                            metrics_out['total_unaligned_bp'] = metric['total_unaligned_bp']
                            metrics_out['total_unaligned_bp_percent'] = round((float(metric['total_unaligned_bp']) / float(metric['total_bp']))*100, 5)
                            metrics_out['unique_on_target_aligned_bp'] = metric['unique_target_aligned_bp']
                            metrics_out['unique_on_target_aligned_bp_percent'] = round((float(metric['unique_target_aligned_bp'])/float(metric['total_bp']))*100, 5)
                            metrics_out['duplicate_on_target_aligned_bp'] = metric['duplicate_target_aligned_bp']
                            metrics_out['duplicate_on_target_aligned_bp_percent'] = round((float(metric['duplicate_target_aligned_bp'])/float(metric['total_bp']))*100, 5)
                            metrics_out['unique_off_target_aligned_bp'] = metric['unique_off_target_aligned_bp']
                            metrics_out['unique_off_target_aligned_bp_percent'] = round((float(metric['unique_off_target_aligned_bp'])/float(metric['total_bp']))*100, 5)
                            metrics_out['duplicate_off_target_aligned_bp'] = metric['duplicate_off_target_aligned_bp']
                            metrics_out['duplicate_off_target_aligned_bp_percent'] = round((float(metric['duplicate_off_target_aligned_bp'])/float(metric['total_bp']))*100, 5)
                    metcsv.close()

        path2 = line['last_succeeded_build.data_directory'] + '/reference_coverage/wingspan_0/'
        if os.path.exists(path2):
            match2 = line['last_succeeded_build.data_directory']  + '/reference_coverage/wingspan_0/*_STATS.txt'
            if glob.glob(match2):
                for metrics_file in glob.glob(match2):
                    with open(metrics_file) as met2csv:
                        read2 = csv.DictReader(met2csv, delimiter="\t")
                        for metric2 in read2:
                            if metric2['minimum_depth'] == '1':
                                metrics_out['mean_depth'] = metric2['mean_depth']
                            if metric2['minimum_depth'] == '20':
                                metrics_out['20X'] = metric2['pc_target_space_covered']
                    met2csv.close()
            w.writerow(metrics_out)

        else:
            print(path, 'directory not found')
exit()


DROOT=$1

ATLAS_TIF="/media/share5/MYK/ATLAS/mouse/annotation_25_half_sagittal_whole.tif"
ATLAS_CSV="/media/share5/MYK/ATLAS/mouse/AllBrainRegions.csv"

# backup previous files
mkdir -p $DROOT/count_bak;mv $DROOT/count_cp_l*.csv $DROOT/count_bak;

for LVL in {1..7};
	do
		echo "count-points-in-region --points $DROOT/CoPosCC_thr_0_6.json --alignment $DROOT/rescaled_*_alignment.json --reference-segmentation $ATLAS_TIF --brain-regions-csv $ATLAS_CSV --output $DROOT/count_cp_l${LVL}.csv --level $LVL";
		count-points-in-region --points $DROOT/CoPosCC_thr_0_6.json --alignment $DROOT/rescaled_*_alignment.json --reference-segmentation $ATLAS_TIF --brain-regions-csv $ATLAS_CSV --output $DROOT/count_cp_l${LVL}.csv --level $LVL;

		# concat
		cat $DROOT/count_cp_l${LVL}.csv >> $DROOT/count_cp_l1-7_all.csv
done;



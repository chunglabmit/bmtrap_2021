DROOT=$1

ATLAS_TIF="/media/share5/MYK/ATLAS/mouse/annotation_25_half_sagittal_whole.tif"
ATLAS_CSV="/media/share5/MYK/ATLAS/mouse/AllBrainRegions.csv"

for LVL in {1..7};
	do
		echo "count-points-in-region --points $DROOT/prediction*_pos.json --alignment $DROOT/rescaled_*_alignment.json --reference-segmentation $ATLAS_TIF --brain-regions-csv $ATLAS_CSV --output $DROOT/output_l${LVL}.csv --xyz --level $LVL";
		count-points-in-region --points $DROOT/prediction*_pos.json --alignment $DROOT/rescaled_*_alignment.json --reference-segmentation $ATLAS_TIF --brain-regions-csv $ATLAS_CSV --output $DROOT/output_l${LVL}.csv --xyz --level $LVL;

		# concat
		cat $DROOT/output_l${LVL}.csv >> $DROOT/output_l1-7_all.csv
done;



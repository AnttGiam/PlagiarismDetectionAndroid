package com.example.plagiomusicale;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;


public class ResultsCheck extends Fragment{

    private TextView plagiarismTW;
    private ProgressBar cosineProgress;
    private TextView cosineTW;
    private ProgressBar soresenProgress;
    private TextView soresenTW;
    private ProgressBar overlapProgress;
    private TextView overlapTW;
    private TextView percentualeTW;
    private TextView tresholdTW;
    private TextView clusteringTW;



    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,Bundle savedInstanceState) {
        Bundle bundle = getArguments();
        View view;
        CheckResults result= (CheckResults) bundle.getSerializable("result");
        view = (View) inflater.inflate(R.layout.results_check, container, false);
        plagiarismTW = view.findViewById(R.id.PlagiarismVerdictTW);
        cosineProgress = view.findViewById(R.id.CosineProgress);
        cosineTW=view.findViewById(R.id.CosineBarText);
        soresenProgress = view.findViewById(R.id.SoresenDiceBar);
        soresenTW = view.findViewById(R.id.SoresenDiceText);
        overlapProgress = view.findViewById(R.id.OverLapBar);
        overlapTW = view.findViewById(R.id.OverLapText);
        percentualeTW = view.findViewById(R.id.PercentualeTW);
        tresholdTW = view.findViewById(R.id.TresholdTW);
        clusteringTW = view.findViewById(R.id.ClusteringTW);



        if (result.isPlagiarism())
            plagiarismTW.setText("DETECTED");
        else
            plagiarismTW.setText("NOT DETECTED");
        String[] cosine = result.getDataResult().getCosine().replace('.',',').split(",");
        System.out.println(cosine[0]);
        int cosineInt = Integer.parseInt(cosine[0]);
        String[] overlap = result.getDataResult().getOverlap().replace('.',',').split(",");
        int overlapInt = Integer.parseInt(overlap[0]);
        String[] soresen = result.getDataResult().getSoresen_dice().replace('.',',').split(",");
        int soresenInt = Integer.parseInt(soresen[0]);
        cosineProgress.setProgress(cosineInt);
        cosineTW.setText(result.getDataResult().getCosine());
        soresenProgress.setProgress(soresenInt);
        soresenTW.setText(result.getDataResult().getSoresen_dice());
        overlapProgress.setProgress(overlapInt);
        overlapTW.setText(result.getDataResult().getOverlap());
        percentualeTW.setText(result.getDataResult().getPercentuage());
        tresholdTW.setText(result.getDataResult().getThreshold());
        clusteringTW.setText(result.getDataResult().getClustering());
        return view;
    }
}

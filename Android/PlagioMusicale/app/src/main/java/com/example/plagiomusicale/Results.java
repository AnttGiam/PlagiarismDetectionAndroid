package com.example.plagiomusicale;

import android.app.DownloadManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import com.fasterxml.jackson.databind.ObjectMapper;

import org.jetbrains.annotations.NotNull;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.Serializable;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import static android.content.Intent.ACTION_GET_CONTENT;


public class Results extends Fragment{

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
    private TextView infoTW;
    private Button torna;
    private Case selezionato;
    private Button download;
    private UserData userData;


    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,Bundle savedInstanceState) {
        Bundle bundle = getArguments();
        View view;
        selezionato= (Case) bundle.getSerializable("selezionato");
        if(selezionato.getHas_verdict()) //Se il caso ha un verdetto caricato, funzioni e layout dedicate a lui
        {
            view = (View) inflater.inflate(R.layout.results_verdict, container, false);
            download=(Button) view.findViewById(R.id.download);
            download.setOnClickListener(new View.OnClickListener(){
                @Override
                public void onClick(View v) {
                    String url = "http://10.0.2.2:5000"+selezionato.getPathFile(); //Path File del Verdetto sul Server
                    System.out.println(url);
                    DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url))
                            .setTitle("Verdetto "+selezionato.getTitle())
                            .setDescription("Scaricando")
                            .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                            .setRequiresCharging(false)
                            .setAllowedOverMetered(true)
                            .setAllowedOverRoaming(true); //Richiesta del File
                    System.out.println(request.toString());
                    DownloadManager downloadManager = (DownloadManager) getActivity().getSystemService(Context.DOWNLOAD_SERVICE);
                    downloadManager.enqueue(request); //Download del File dal Server
                }
            });
        }
        else
            view = (View) inflater.inflate(R.layout.results, container, false);
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
        infoTW= view.findViewById(R.id.infoTW);
        torna = (Button) view.findViewById(R.id.torna);

        if (selezionato.getIs_plagiarism())
            plagiarismTW.setText("DETECTED");
        else
            plagiarismTW.setText("NOT DETECTED");
        String[] cosine = selezionato.getDataResult().getCosine().replace('.',',').split(",");
        int cosineInt = Integer.parseInt(cosine[0]);
        String[] overlap = selezionato.getDataResult().getOverlap().replace('.',',').split(",");
        int overlapInt = Integer.parseInt(overlap[0]);
        String[] soresen = selezionato.getDataResult().getSoresen_dice().replace('.',',').split(",");
        int soresenInt = Integer.parseInt(soresen[0]);
        cosineProgress.setProgress(cosineInt);
        cosineTW.setText(selezionato.getDataResult().getCosine());
        soresenProgress.setProgress(soresenInt);
        soresenTW.setText(selezionato.getDataResult().getSoresen_dice());
        overlapProgress.setProgress(overlapInt);
        overlapTW.setText(selezionato.getDataResult().getOverlap());
        percentualeTW.setText(selezionato.getDataResult().getPercentuage());
        tresholdTW.setText(selezionato.getDataResult().getThreshold());
        clusteringTW.setText(selezionato.getDataResult().getClustering());
        infoTW.setText(selezionato.getInfo());

        torna.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                FragmentTransaction ft =  getActivity().getSupportFragmentManager().beginTransaction();
                Bundle bundle = new Bundle();
                bundle.putString("mailUser",getArguments().getString("mailUser"));
                ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_OPEN);
                ViewCases fragment = new ViewCases();
                ft.replace(R.id.fragment_container, fragment);
                ft.commit();
            }
        });


        return view;
    }
}

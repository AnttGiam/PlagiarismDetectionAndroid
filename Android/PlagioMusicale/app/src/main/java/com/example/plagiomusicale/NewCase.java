package com.example.plagiomusicale;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.Serializable;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Headers;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static android.content.Intent.ACTION_GET_CONTENT;

public class NewCase extends Fragment {

    private EditText title;
    private EditText firstSongName;
    private EditText secondSongName;
    private RelativeLayout uploadSong1;
    private RelativeLayout uploadSong2;
    private EditText info;
    private RadioGroup radioGroup;
    private RelativeLayout uploadVerdict;
    private Button postCase;
    private Intent myFile;
    private String song1Path;
    private String song2Path;
    private TextView song1f;
    private TextView song2f;
    private String verdictPath;
    private TextView verdictf;
    private String verdictStr;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.new_case,container,false);
        title=view.findViewById(R.id.title);
        firstSongName=view.findViewById(R.id.song1Name);
        secondSongName=view.findViewById(R.id.song2Name);
        info=view.findViewById(R.id.info);
        radioGroup=view.findViewById(R.id.verdictRadio);
        postCase=view.findViewById(R.id.postCase);
        song1f=view.findViewById(R.id.song1f);
        song2f=view.findViewById(R.id.song2f);
        verdictf=view.findViewById(R.id.verdictf);
        uploadSong1=view.findViewById(R.id.uploadSong1);
        uploadSong2=view.findViewById(R.id.uploadSong2);
        uploadVerdict=view.findViewById(R.id.uploadVerdict);
        verdictStr="NoTrial";
        uploadSong1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                myFile = new Intent(ACTION_GET_CONTENT);
                myFile.setType("*/*");
                uploadFirstSong.launch(myFile);
            }
        });

        uploadSong2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                myFile = new Intent(ACTION_GET_CONTENT);
                myFile.setType("*/*");
                uploadSecondSong.launch(myFile);

            }
        });


        radioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener()
        {
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                switch(checkedId){
                    case R.id.NoTrial:
                        verdictStr="NoTrial";
                        uploadVerdict.setOnClickListener(new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {

                            }
                        });
                        break;
                    case R.id.hasTrial:
                        verdictStr="hasTrial";
                        uploadVerdict.setOnClickListener(new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {

                            }
                        });
                        break;
                    case R.id.hasTrialAndVerdict:
                        verdictStr="hasTrialAndVerdict";
                        uploadVerdict.setOnClickListener(new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                myFile = new Intent(ACTION_GET_CONTENT);
                                myFile.setType("*/*");
                                uploadVerdictFile.launch(myFile);

                            }
                        });
                        break;
                }
            }
        });

        postCase.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        OkHttpClient okHttpClient = new OkHttpClient();
                        InputStream in = null;
                        String path = "/mnt/sdcard/";
                        File file1 = new File(path+""+song1Path);
                        File file2 = new File(path+""+song2Path);
                        File file3 = new File(path+""+verdictPath);
                        if (file1.isFile()) { //Prima Canzone
                            System.out.println("File1");
                        } else System.out.println("no FIle1");
                        if (file2.isFile()) { //Seconda Canzone
                            System.out.println("File2");
                        } else System.out.println("no FIle2");
                        RequestBody fileBody1 = RequestBody.create(MediaType.parse("application/octet-stream"), file1);
                        RequestBody fileBody2 = RequestBody.create(MediaType.parse("application/octet-stream"), file2);
                        RequestBody requestBody;
                        if(verdictStr=="hasTrialAndVerdict") { //Se ha il verdetto, aggiungerlo
                            RequestBody fileBody3 = RequestBody.create(MediaType.parse("application/octet-stream"), file3);
                            requestBody = new MultipartBody.Builder()
                                    .setType(MultipartBody.FORM)
                                    .addPart(Headers.of(
                                            "Content-Disposition",
                                            "form-data; name=\"song1\"; filename=\"" + song1f.getText().toString() + "\""), fileBody1)
                                    .addPart(Headers.of(
                                            "Content-Disposition",
                                            "form-data; name=\"song2\"; filename=\"" + song2f.getText().toString() + "\""), fileBody2)
                                    .addPart(Headers.of(
                                            "Content-Disposition",
                                            "form-data; name=\"verdict\"; filename=\"" + verdictf.getText().toString() + "\""), fileBody3)
                                    .addFormDataPart("title", title.getText().toString())
                                    .addFormDataPart("first_song_name", firstSongName.getText().toString())
                                    .addFormDataPart("second_song_name", secondSongName.getText().toString())
                                    .addFormDataPart("info", info.getText().toString())
                                    .addFormDataPart("mail", getArguments().getString("mailUser"))
                                    .addFormDataPart("radioChoice", verdictStr)
                                    .build();
                        }
                        else //Non ha il verdetto
                        {
                            requestBody = new MultipartBody.Builder()
                                    .setType(MultipartBody.FORM)
                                    .addPart(Headers.of(
                                            "Content-Disposition",
                                            "form-data; name=\"song1\"; filename=\"" + song1f.getText().toString() + "\""), fileBody1)
                                    .addPart(Headers.of(
                                            "Content-Disposition",
                                            "form-data; name=\"song2\"; filename=\"" + song2f.getText().toString() + "\""), fileBody2)
                                    .addFormDataPart("title", title.getText().toString())
                                    .addFormDataPart("first_song_name", firstSongName.getText().toString())
                                    .addFormDataPart("second_song_name", secondSongName.getText().toString())
                                    .addFormDataPart("info", info.getText().toString())
                                    .addFormDataPart("mail", getArguments().getString("mailUser"))
                                    .addFormDataPart("radioChoice", verdictStr)
                                    .build();
                        }
                        String url = "http://10.0.2.2:5000/new_sentence_no_check/newMobile";
                        Request request = new Request.Builder()
                                .url(url)
                                .post(requestBody)
                                .build();
                        Call call = okHttpClient.newCall(request); //Invia i dati al Server

                        call.enqueue(new Callback() {
                            @Override
                            public void onFailure(Call call, IOException e) {
                                e.printStackTrace();
                                Log.e("text", "failure upload!");
                            }

                            @Override
                            public void onResponse(Call call, Response response) throws IOException {
                                Log.i("text", "success upload!");
                                String json = response.body().string();
                                Bundle bundle = new Bundle();
                                bundle.putString("mailUser",getArguments().getString("mailUser"));
                                FragmentTransaction ft =  getActivity().getSupportFragmentManager().beginTransaction();
                                ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_OPEN);
                                ViewCases fragment = new ViewCases();
                                fragment.setArguments(bundle);
                                ft.replace(R.id.fragment_container, fragment);
                                ft.commit();
                            }
                        });
                    }

                }).start();

            }
        });
        return view;
    }

    ActivityResultLauncher<Intent> uploadSecondSong = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {
                        Intent data = result.getData();
                        song2Path = data.getData().getPath();
                        String[] song = song2Path.split("plagio/");
                        song2f.setText(song[1]);
                        String[] secondopath1 = song2Path.split("/0");
                        song2Path = secondopath1[1];

                    }
                }
            });

    ActivityResultLauncher<Intent> uploadFirstSong = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {
                        Intent data = result.getData();
                        song1Path = data.getData().getPath();
                        String[] song = song1Path.split("plagio/");
                        song1f.setText(song[1]);
                        String[] primopath1 = song1Path.split("/0");
                        song1Path = primopath1[1];
                    }
                }
            });

    ActivityResultLauncher<Intent> uploadVerdictFile = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {
                        Intent data = result.getData();
                        verdictPath = data.getData().getPath();
                        String[] song = verdictPath.split("/");
                        verdictf.setText(song[song.length-1]);
                        String[] primopath1 = verdictPath.split("/0");
                        verdictPath = primopath1[1];
                    }
                }
            });
}

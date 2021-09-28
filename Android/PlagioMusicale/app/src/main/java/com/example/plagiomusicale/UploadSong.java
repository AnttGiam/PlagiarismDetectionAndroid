package com.example.plagiomusicale;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import com.fasterxml.jackson.databind.ObjectMapper;

import org.jetbrains.annotations.NotNull;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.Serializable;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Headers;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import pl.droidsonroids.gif.GifImageView;

import static android.app.Activity.RESULT_OK;
import static android.content.Intent.ACTION_GET_CONTENT;
import static android.content.pm.PackageManager.PERMISSION_GRANTED;
import static android.os.Environment.getDownloadCacheDirectory;
import static android.os.Environment.getExternalStorageState;

public class UploadSong extends Fragment {

    private RelativeLayout uploadSong1;
    private RelativeLayout uploadSong2;
    private Button uploadSongs;
    private TextView song1;
    private TextView song2;
    private Intent myFile;
    private String path1;
    private String path2;
    private String primopath;
    private String secondopath;
    private CheckResults result;
    private Bundle datiUtente;
    private View view;


    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.upload_song, container, false);
        datiUtente = getArguments();
        uploadSong1 = (RelativeLayout) view.findViewById(R.id.uploadSong1);
        uploadSong2 = (RelativeLayout) view.findViewById(R.id.uploadSong2);
        uploadSongs = (Button) view.findViewById(R.id.uploadSongs);
        song1 = (TextView) view.findViewById(R.id.song1);
        song2 = (TextView) view.findViewById(R.id.song2);

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
        
        uploadSongs.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                FragmentTransaction ft =  getActivity().getSupportFragmentManager().beginTransaction();
                ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_OPEN);
                Loading fragment = new Loading();
                ft.replace(R.id.fragment_container, fragment);
                ft.addToBackStack(null);
                ft.commit();
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        OkHttpClient okHttpClient = new OkHttpClient();
                        InputStream in = null;
                        String path = "/mnt/sdcard/";
                        File file1 = new File(path+""+primopath);
                        File file2 = new File(path+""+secondopath);
                        if (file1.isFile()) {
                            System.out.println("File1");
                        } else System.out.println("no FIle1");
                        if (file2.isFile()) {
                            System.out.println("File2");
                        } else System.out.println("no FIle2");
                        RequestBody fileBody1 = RequestBody.create(MediaType.parse("application/octet-stream"), file1);
                        RequestBody fileBody2 = RequestBody.create(MediaType.parse("application/octet-stream"), file2);
                        RequestBody requestBody = new MultipartBody.Builder()
                                .setType(MultipartBody.FORM)
                                .addPart(Headers.of(
                                        "Content-Disposition",
                                        "form-data; name=\"song1\"; filename=\"" + song1.getText().toString() + "\""), fileBody1)
                                .addPart(Headers.of(
                                        "Content-Disposition",
                                        "form-data; name=\"song2\"; filename=\"" + song2.getText().toString() + "\""), fileBody2)
                                .build();

                        String url = "http://10.0.2.2:5000/upload_songsMobile";
                        Request request = new Request.Builder()
                                .url(url)
                                .post(requestBody)
                                .build();
                        Call call = okHttpClient.newCall(request);

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

                                Log.i("success........", "success" + json);
                                ObjectMapper mapper = new ObjectMapper();
                                result = mapper.readValue(json,CheckResults.class);
                                System.out.println(result);
                                FragmentTransaction ft =  getActivity().getSupportFragmentManager().beginTransaction();
                                ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_OPEN);
                                ResultsCheck fragment = new ResultsCheck();
                                Bundle bundle = new Bundle();
                                bundle.putSerializable("result", (Serializable) result);
                                fragment.setArguments(bundle);
                                ft.replace(R.id.fragment_container, fragment);
                                ft.addToBackStack(null);
                                ft.commit();
                            }
                        });
                    }

                }).start();

            }
        });


        return view;
    }


    ActivityResultLauncher<Intent> uploadFirstSong = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {
                        Intent data = result.getData();
                        path1 = data.getData().getPath();
                        String[] song = path1.split("plagio/");
                        song1.setText(song[1]);
                        String[] primopath1 = path1.split("/0");
                        primopath = primopath1[1];

                    }
                }
            });

    ActivityResultLauncher<Intent> uploadSecondSong = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {
                        Intent data = result.getData();
                        path2 = data.getData().getPath();
                        String[] song = path2.split("plagio/");
                        song2.setText(song[1]);
                        String[] secondopath1 = path2.split("/0");
                        secondopath = secondopath1[1];

                    }
                }
            });

}



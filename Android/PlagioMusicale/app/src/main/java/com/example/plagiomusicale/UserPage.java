package com.example.plagiomusicale;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
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

import static android.content.Intent.ACTION_GET_CONTENT;

public class UserPage extends Fragment {
    private UserData userData;
    private EditText userInfo;
    private EditText mailInfo;
    private EditText expertise;
    private Button updateBT;
    private Intent myFile;
    private String imagePath;
    private String image1;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.user_page,container,false);
        userInfo=view.findViewById(R.id.userNameInfoET);
        mailInfo=view.findViewById(R.id.emailInfoET);
        expertise=view.findViewById(R.id.expertiseInfoET);
        updateBT=view.findViewById(R.id.updateProfile);
        updateBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        OkHttpClient okHttpClient = new OkHttpClient();
                        InputStream in = null;
                        String path = "/mnt/sdcard/";
                        RequestBody requestBody = new MultipartBody.Builder()
                                    .setType(MultipartBody.FORM)
                                    .addFormDataPart("username", userInfo.getText().toString())
                                    .addFormDataPart("expertise", expertise.getText().toString())
                                    .addFormDataPart("mail",getArguments().getString("mailUser"))
                                    .build();
                        System.out.println("INVIATA MAIL "+getArguments().getString("mailUser"));
                        String url = "http://10.0.2.2:5000/accountUpdateMobile";
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
                                FragmentTransaction ft =  getActivity().getSupportFragmentManager().beginTransaction();
                                ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_OPEN);
                                UserPage fragment = new UserPage();
                                fragment.setArguments(getArguments());
                                ft.replace(R.id.fragment_container, fragment);
                                ft.addToBackStack(null);
                                ft.commit();
                            }
                        });
                    }

                }).start();
            }
        });

        System.out.println("MAIL DA PARAMETRO:"+getArguments().getString("mailUser"));
        new UserTask().execute(getArguments().getString("mailUser"));
        return view;

    }


    class UserTask extends AsyncTask<String,Integer,Integer> {

    private boolean terminatoUser;

        @Override
        protected void onPreExecute() {
            terminatoUser=false;
            super.onPreExecute();
        }

        @Override
        protected Integer doInBackground(String... strings) {
            OkHttpClient client = new OkHttpClient();
            String url = "http://10.0.2.2:5000/accountMobile?mail="+strings[0];
            System.out.println(url);
            System.out.println(strings.length+" LUNGHEZZA PARAMETRI");
            Request request = new Request.Builder().url(url).build();
            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(@NotNull Call call, @NotNull IOException e) {
                    e.printStackTrace();
                }

                @Override
                public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                    String jsonStr = response.body().string();
                    ObjectMapper mapper = new ObjectMapper();
                    userData = mapper.readValue(jsonStr,UserData.class);
                    System.out.println("DOWNLOAD DI "+ userData);
                    terminatoUser=true;
                }
            });
            while(!terminatoUser){
                System.out.println("Non ho ancora finito");
            }
            return 0;
        }

        @Override
        protected void onPostExecute(Integer integer) {
            super.onPostExecute(integer);
            while(!terminatoUser){}
            userInfo.setText(userData.getUsername());
            mailInfo.setText(userData.getEmail());
            expertise.setText(userData.getExpertise());
            System.out.println("HO FINITO E HO TROVATO L'UTENTE: "+userData.getFirst_name());
        }
    }

    class UpdateUser extends AsyncTask<String,Integer,Integer> {

        private boolean terminatoUser;

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            terminatoUser=false;
        }

        @Override
        protected Integer doInBackground(String... strings) {
            OkHttpClient client = new OkHttpClient();
            String url = "http://10.0.2.2:5000/accountMobile?mail="+strings[0];
            System.out.println(url);
            System.out.println(strings.length+" LUNGHEZZA PARAMETRI");
            Request request = new Request.Builder().url(url).build();
            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(@NotNull Call call, @NotNull IOException e) {
                    e.printStackTrace();
                }

                @Override
                public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                    String jsonStr = response.body().string();
                    ObjectMapper mapper = new ObjectMapper();
                    userData = mapper.readValue(jsonStr,UserData.class);
                    System.out.println("DOWNLOAD DI "+ userData);
                    terminatoUser=true;
                }
            });
            while(!terminatoUser){}
            return 0;
        }

        @Override
        protected void onPostExecute(Integer integer) {
            super.onPostExecute(integer);
            while(!terminatoUser){}
            userInfo.setText(userData.getUsername());
            mailInfo.setText(userData.getEmail());
            expertise.setText(userData.getExpertise());
            System.out.println("HO FINITO E HO TROVATO L'UTENTE: "+userData.getFirst_name());
        }
    }
}
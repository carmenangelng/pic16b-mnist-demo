## Deploying webapp to Google Cloud from GitHub repository

1. Redeem the free student google cloud credit by following instructions from announcement email last Friday.

2. Make a fork of this repository.

### Testing locally
3. Copy this repo into your local computer. Both `git clone` and downloading the zip file works.

4. Inside the code folder `pic16b-mnist-demo`, run 
 ```
conda activate PIC16B-25W
python app.py
```
to make sure you're in the correct directory and the code and dash is working. 
Once you've checked that the website is working locally, you can close the dash app.

  **FAQ**: If you get an error message like "port 5000 is in use", make sure no other dash app is running in your laptop, and try changing the port.

### Deploying the app

5. Now, go to Google Cloud console (https://console.cloud.google.com/) and create a new project. 
Project ID can be anything, and the organization can be "no organization". 
The most important thing is that the __billing account is connected to your "education" billing account__ (which is where your free credit should be at).

6. Enable IAM API.
  - Go to "APIs & Servies" menu (you can type it into the search bar at the top).
  - Press "+ Enable APIs and Services" button.
  - Search "Identity and Access Management (IAM) API", and enable it (not to be confused with IAM Service Account Credentials API).
7. Create the cloud service.
  - Go to "Cloud Run" menu.
  - Press "+ Deploy Container" button, then "Service".
  - Select "Continuously deploy new revisions from a source repository".
  - Click on "Set up with cloud build"
    - Select your GitHub repository.
      - You may have to authenticate to GitHub first.
    - Select docker build option.
  - For region, let's use "us-west-1".
  - For revision autoscaling, let's use 0 to 5 for this class, as this is supposed to be a small app.
  - For Authentication, select "Allow unauthenticated invocations".
  - If everything goes smoothly, your service should run at some url that looks like https://mnist-[...]-wn.a.run.app/. You will have to wait several minutes for your app to be built first.

8. You can update your app by pushing to the `main` branch on GitHub.
   
**FAQ**: If you see trigger failed error, you might have missed enabling IAM API. You can go enable it, then trigger the build again by pushing something to the repository. 

**FAQ**: Can I change the weird url? Looks like you can but it's a lot more involved than I initially thought: https://cloud.google.com/run/docs/mapping-custom-domains

**FAQ**: You can deploy multiple times in the same project. You can delete the deployed app from the "Services" tab of the "Cloud Run" menu. Keep your eyes on Billing tab every several days, and try to avoid overcharges -- it often won't be a major issue for lightweight apps, but things can happen. Nothing specifically occurs other than you will no longer be able to use Google Cloud Platform if you use all the credits.



## Notes

1. When you're working on the web app homework or project, I fully expect you to copy the files from this git repo and modify it.
   You may need to change `requirements.txt` based on packages and their versions you use, but I recommend keeping the `Dockerfile` and `Procfile` as is (unless you have a good understanding of what you're doing!).


<p>This project was an assignment that was given by the university to develop a voting system that is to be used for any election that will be carried out in the university. The system was also supposed to include concepts of blockchain.</p>
<p>This was my attempt of the proposed assignment.</p>
<h1>The Project Description</h1>
<p>The system was developed in python with the Flask framework. The system encorporated assymetric cryptographic encryption to ensure that once a vote has been casted it is kept secure and only the user that has voted, can retrieve their vote.</p>
<p>The system assigns a public and private key to a user upon casting their vote, and their private key will be used when retreiving their casted vote.</p>
<h1>How It Works</h1>
<ul>
<li>Once a user has created an account and logged in, they can begin the election process.</li><br>
<img src="https://user-images.githubusercontent.com/63863253/190230930-e165f66b-5832-42aa-a125-fbb9bfd46751.png">
<li>First, The user will be required to verify themselves, only verified users can be allowed to vote. A secret key is sent to the user's email address and upon entering the correct key, the user will be verified and is redirected to the election page.</li><br>
<img src="https://user-images.githubusercontent.com/63863253/190231279-f816382b-b80a-4c87-a2f0-541ba5aa96a6.png">
<li>Secondly, the election selects the candidates and presents them to the logged in user, then the user can click on the candidate they want to cast their vote for.</li><br>
<img src="https://user-images.githubusercontent.com/63863253/190231459-b95b9c51-ecdb-4671-b78c-414eb7cf40d3.png">
<img src="https://user-images.githubusercontent.com/63863253/190231694-089cd537-e96c-4287-885e-2350506cdf98.png">
<li>Thirdly, the vote is recorded and secured and the user is sent the private key in their email address that they'll use if they want to retreive their casted vote.</li><br>
<img src="https://user-images.githubusercontent.com/63863253/190231791-20990368-4d15-44eb-a297-c92214bfe954.png">
<li>Finally, when the user wants to retreive their vote, they'll enter the sent private key and upon confirmation, a unique secret key is sent to the users email address, and upon successfull confirmation, the casted vote is sent to the user's email address.</li><br>
<img src="https://user-images.githubusercontent.com/63863253/190232002-57d8e028-0674-4166-9dec-097b2264467a.png">
<img src="https://user-images.githubusercontent.com/63863253/190232592-3ec92665-2c87-45bc-85cf-c863ec5c7ae8.png">
<img src="https://user-images.githubusercontent.com/63863253/190232275-fe297854-b977-418e-9076-69d3f70d3f3b.png">
</ul>
<p>Once the user has casted their vote, they cannot be allowed to cast another vote, so only one vote per user.</p>
<img src="https://user-images.githubusercontent.com/63863253/190233988-4a8a3d36-6839-437b-a610-152d4df07345.png">

fig = plt.figure(figsize=(12*cm, 10*cm))
mproj = ccrs.Mollweide(central_longitude=-160)
ax = fig.add_subplot(nrow, ncol, i, projection=mproj)